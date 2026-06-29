"""webhook/services/monitoring/health.py — فحوصات صحة الخدمات"""
from __future__ import annotations
import asyncio, logging, os, time
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger("alazab.monitoring.health")
_start_time = time.time()

@dataclass
class ServiceHealth:
    name: str
    status: str
    latency_ms: Optional[float] = None
    detail: str = ""
    checked_at: float = field(default_factory=time.time)

async def check_rasa(url: str, timeout: float = 3.0) -> ServiceHealth:
    try:
        import httpx
        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=timeout) as c:
            r = await c.get(f"{url}/")
        ms = round((time.perf_counter() - start) * 1000, 1)
        return ServiceHealth("rasa", "up" if r.status_code == 200 else "degraded", ms)
    except Exception as exc:
        return ServiceHealth("rasa", "down", detail=str(exc)[:120])

async def check_redis() -> ServiceHealth:
    try:
        import redis as _r
        start = time.perf_counter()
        r = _r.Redis(host=os.getenv("REDIS_HOST","127.0.0.1"), port=int(os.getenv("REDIS_PORT","6379")),
                      password=os.getenv("REDIS_PASSWORD") or None, socket_connect_timeout=2, socket_timeout=2)
        r.ping()
        return ServiceHealth("redis", "up", round((time.perf_counter()-start)*1000,1))
    except Exception as exc:
        return ServiceHealth("redis", "down", detail=str(exc)[:120])

async def check_supabase() -> ServiceHealth:
    url = os.getenv("SUPABASE_URL","").strip()
    key = (os.getenv("SUPABASE_SERVICE_ROLE_KEY","") or os.getenv("SUPABASE_SECRET_KEY","")).strip()
    if not (url and key): return ServiceHealth("supabase", "unknown", detail="credentials not set")
    try:
        from supabase import create_client
        start = time.perf_counter()
        client = create_client(url, key)
        client.table("bot_settings").select("id").limit(1).execute()
        return ServiceHealth("supabase", "up", round((time.perf_counter()-start)*1000,1))
    except Exception as exc:
        return ServiceHealth("supabase", "down", detail=str(exc)[:120])

async def check_actions(url: str = "http://127.0.0.1:5055", timeout: float = 3.0) -> ServiceHealth:
    try:
        import httpx
        start = time.perf_counter()
        async with httpx.AsyncClient(timeout=timeout) as c:
            r = await c.get(f"{url}/health")
        return ServiceHealth("actions", "up" if r.status_code == 200 else "degraded", round((time.perf_counter()-start)*1000,1))
    except Exception as exc:
        return ServiceHealth("actions", "down", detail=str(exc)[:80])

async def full_health_check(rasa_url: str) -> dict:
    import psutil
    rasa, redis_h, sb, actions = await asyncio.gather(
        check_rasa(rasa_url), check_redis(), check_supabase(), check_actions(),
    )
    services = {s.name: s for s in (rasa, redis_h, sb, actions)}
    critical = all(s.status == "down" for s in (rasa, redis_h))
    any_down = any(s.status == "down" for s in services.values())
    overall = "critical" if critical else ("degraded" if any_down else "ok")
    process = psutil.Process(os.getpid()); mem = process.memory_info()
    return {
        "status": overall, "version": "4.1.0",
        "services": {n: {"status": s.status, "latency_ms": s.latency_ms, "detail": s.detail or None} for n, s in services.items()},
        "channels": {
            "website": True,
            "whatsapp": bool(os.getenv("WHATSAPP_TOKEN") or os.getenv("META_TOKEN")),
            "messenger": bool(os.getenv("FB_PAGE_ACCESS_TOKEN")),
            "telegram": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
        },
        "system": {
            "memory_mb": round(mem.rss/(1024*1024),1),
            "cpu_percent": psutil.cpu_percent(interval=None),
            "load_avg": list(os.getloadavg()) if hasattr(os,"getloadavg") else None,
            "uptime_seconds": round(time.time()-_start_time),
        },
    }
