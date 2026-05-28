"""
webhook/services/monitoring/metrics.py
=======================================
عدادات في الذاكرة لمعرفة أداء كل endpoint وكل قناة.
خفيف — بدون Prometheus، يُعيد البيانات عبر /health/details.
"""
from __future__ import annotations

import time
from collections import defaultdict, deque
from threading import Lock
from typing import Deque

_lock  = Lock()
_start = time.time()

# counters
_channel_counts:  dict[str, int]       = defaultdict(int)
_endpoint_counts: dict[str, int]       = defaultdict(int)
_error_counts:    dict[str, int]       = defaultdict(int)

# latency sliding window (last 1000 requests per endpoint)
_latencies: dict[str, Deque[float]] = defaultdict(lambda: deque(maxlen=1000))


def inc_channel(channel: str) -> None:
    with _lock:
        _channel_counts[channel] += 1


def inc_endpoint(path: str, latency_ms: float, is_error: bool = False) -> None:
    with _lock:
        _endpoint_counts[path] += 1
        _latencies[path].append(latency_ms)
        if is_error:
            _error_counts[path] += 1


def snapshot() -> dict:
    with _lock:
        endpoint_stats = {}
        for path, count in _endpoint_counts.items():
            lats = list(_latencies.get(path, []))
            endpoint_stats[path] = {
                "count":        count,
                "errors":       _error_counts.get(path, 0),
                "p50_ms":       _percentile(lats, 50),
                "p95_ms":       _percentile(lats, 95),
                "p99_ms":       _percentile(lats, 99),
            }
        return {
            "uptime_seconds": round(time.time() - _start),
            "channels":       dict(_channel_counts),
            "endpoints":      endpoint_stats,
        }


def _percentile(data: list[float], pct: int) -> float | None:
    if not data:
        return None
    s = sorted(data)
    idx = int(len(s) * pct / 100)
    return round(s[min(idx, len(s)-1)], 1)
