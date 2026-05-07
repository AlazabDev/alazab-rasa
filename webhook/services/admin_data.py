"""
webhook/services/admin_data.py — Admin Dashboard Data Layer
=============================================================
Manages admin data (conversations, uploads, settings, integrations, logs).
Currently uses JSON file storage — ready for Redis/PostgreSQL migration.
"""

from __future__ import annotations

import json
import logging
import os
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Optional

from ..config import ADMIN_DATA_FILE, DEFAULT_ADMIN_DATA
from ..utils import serialize_attachment

logger = logging.getLogger("alazab.webhook.admin")

_admin_data_lock = Lock()
_stats: dict[str, int] = defaultdict(int)
_start_time = time.time()


# ══════════════════════════════════════════════════════════════
#  Stats
# ══════════════════════════════════════════════════════════════
def count(channel: str) -> None:
    """Increment message counter for the given channel."""
    _stats[channel] += 1


def admin_stats_payload() -> dict[str, Any]:
    """Build stats summary for admin dashboard."""
    data = load_admin_data()
    conversations = data.get("conversations", [])
    uploads = data.get("uploads", [])
    messages = sum(len(item.get("messages", [])) for item in conversations)
    today_prefix = datetime.now(timezone.utc).date().isoformat()
    return {
        "conversations": len(conversations),
        "messages": messages,
        "uploads": len(uploads),
        "today": sum(
            1 for item in conversations
            if str(item.get("created_at", "")).startswith(today_prefix)
        ),
        "message_counts": dict(_stats),
        "total": sum(_stats.values()),
        "uptime_seconds": round(time.time() - _start_time),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def get_start_time() -> float:
    """Return the server start time for uptime calculations."""
    return _start_time


def get_stats() -> dict[str, int]:
    """Return the current message stats dict."""
    return dict(_stats)


# ══════════════════════════════════════════════════════════════
#  Persistence
# ══════════════════════════════════════════════════════════════
def load_admin_data() -> dict[str, Any]:
    """Load admin data from JSON file with defaults merge."""
    if not ADMIN_DATA_FILE.exists():
        return json.loads(json.dumps(DEFAULT_ADMIN_DATA))
    try:
        with _admin_data_lock:
            data = json.loads(ADMIN_DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        logger.exception("Failed to read admin data file")
        return json.loads(json.dumps(DEFAULT_ADMIN_DATA))
    merged = json.loads(json.dumps(DEFAULT_ADMIN_DATA))
    for key, value in data.items():
        if key == "settings" and isinstance(value, dict):
            merged["settings"] = {**merged["settings"], **value}
        else:
            merged[key] = value
    return merged


def save_admin_data(data: dict[str, Any]) -> None:
    """Atomically save admin data to JSON file."""
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    tmp_path = ADMIN_DATA_FILE.with_name(f".{ADMIN_DATA_FILE.name}.{uuid.uuid4().hex}.tmp")
    with _admin_data_lock:
        try:
            tmp_path.write_text(payload, encoding="utf-8")
            os.replace(tmp_path, ADMIN_DATA_FILE)
        finally:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)


# ══════════════════════════════════════════════════════════════
#  Conversation Recording
# ══════════════════════════════════════════════════════════════
async def record_conversation(
    sender_id: str,
    user_text: str,
    responses: list[dict[str, Any]],
    *,
    channel: str,
    brand: Optional[str],
    attachment: Optional[dict[str, Any]] = None,
    dispatch_integrations_fn=None,
) -> None:
    """Record a conversation message and dispatch integrations."""
    data = load_admin_data()
    conversations = data.setdefault("conversations", [])
    now = datetime.now(timezone.utc).isoformat()
    conv = next((item for item in conversations if item.get("session_id") == sender_id), None)
    is_new_conversation = conv is None
    if not conv:
        conv = {
            "id": str(uuid.uuid4()),
            "session_id": sender_id,
            "brand": brand,
            "channel": channel,
            "created_at": now,
            "last_message_at": now,
            "messages": [],
        }
        conversations.insert(0, conv)

    conv["last_message_at"] = now
    conv["brand"] = brand or conv.get("brand")
    conv["channel"] = channel or conv.get("channel")
    user_message = {
        "id": str(uuid.uuid4()),
        "role": "user",
        "content": user_text,
        "created_at": now,
    }
    if attachment:
        safe_attachment = serialize_attachment(attachment)
        user_message["attachments"] = [safe_attachment]
    conv.setdefault("messages", []).append(user_message)

    if attachment:
        uploads = data.setdefault("uploads", [])
        uploads.insert(
            0,
            {
                "id": str(uuid.uuid4()),
                "conversation_id": conv["id"],
                "session_id": sender_id,
                "message_id": user_message["id"],
                "brand": brand,
                "channel": channel,
                "created_at": now,
                "note": user_text,
                **attachment,
            },
        )
        data["uploads"] = uploads[:1000]

    assistant_messages: list[dict[str, Any]] = []
    for response in responses:
        text = response.get("text") if isinstance(response, dict) else None
        if text:
            assistant_message = {
                "id": str(uuid.uuid4()),
                "role": "assistant",
                "content": text,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            buttons = response.get("buttons") if isinstance(response, dict) else None
            if isinstance(buttons, list):
                safe_buttons = []
                for button in buttons:
                    if not isinstance(button, dict):
                        continue
                    title = str(button.get("title") or "").strip()
                    btn_payload = str(button.get("payload") or "").strip()
                    url = str(button.get("url") or "").strip()
                    if not title:
                        continue
                    safe_button: dict[str, str] = {"title": title}
                    if btn_payload:
                        safe_button["payload"] = btn_payload
                    if url:
                        safe_button["url"] = url
                    safe_buttons.append(safe_button)
                if safe_buttons:
                    assistant_message["buttons"] = safe_buttons
            assistant_messages.append(assistant_message)
            conv["messages"].append(assistant_message)

    conv["message_count"] = len(conv.get("messages", []))
    data["conversations"] = conversations[:500]
    save_admin_data(data)

    if dispatch_integrations_fn:
        integration_payload = {
            "conversation": integration_conversation_payload(conv),
            "message": user_message,
            "responses": assistant_messages,
        }
        if is_new_conversation:
            await dispatch_integrations_fn("conversation.started", integration_payload)
        await dispatch_integrations_fn("message.created", integration_payload)


def integration_conversation_payload(conversation: dict[str, Any]) -> dict[str, Any]:
    """Build a payload for integration events."""
    return {
        "id": conversation.get("id"),
        "session_id": conversation.get("session_id"),
        "brand": conversation.get("brand"),
        "channel": conversation.get("channel"),
        "created_at": conversation.get("created_at"),
        "last_message_at": conversation.get("last_message_at"),
        "message_count": conversation.get("message_count", len(conversation.get("messages", []))),
    }
