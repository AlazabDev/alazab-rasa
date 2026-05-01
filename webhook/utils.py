"""
webhook/utils.py — Shared Utility Functions
=============================================
"""

from __future__ import annotations

import re
import uuid
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

from fastapi import Request

from .config import (
    BRAND_ALIAS_MAP,
    BRAND_PATH_MAP,
    BRAND_PROFILES,
    PUBLIC_BASE_URL,
    SITE_BRAND_MAP,
    UPLOADS_ROOT,
)
import os


# ══════════════════════════════════════════════════════════════
#  Serialization
# ══════════════════════════════════════════════════════════════
def jsonable(value: Any) -> Any:
    """Recursively convert non-JSON-serializable types."""
    if isinstance(value, dict):
        return {str(k): jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [jsonable(item) for item in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, uuid.UUID):
        return str(value)
    return value


# ══════════════════════════════════════════════════════════════
#  Path Safety
# ══════════════════════════════════════════════════════════════
def is_relative_to(child: Path, parent: Path) -> bool:
    """التحقق من أن المسار يقع داخل المجلد المسموح به (حماية من Path Traversal)."""
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except (ValueError, RuntimeError):
        return False


# ══════════════════════════════════════════════════════════════
#  Text / Phone
# ══════════════════════════════════════════════════════════════
def phone_digits(value: Any) -> str:
    return re.sub(r"\D+", "", str(value or ""))


def sanitize_filename(filename: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", filename).strip("._")
    return cleaned or "upload.bin"


# ══════════════════════════════════════════════════════════════
#  URL / Host helpers
# ══════════════════════════════════════════════════════════════
def extract_hostname(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    first_value = value.split(",")[0].strip()
    if not first_value:
        return None
    parsed = urlparse(first_value if "://" in first_value else f"https://{first_value}")
    hostname = parsed.hostname or parsed.path
    return hostname.lower() if hostname else None


def extract_path(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    first_value = value.split(",")[0].strip()
    if not first_value:
        return None
    parsed = urlparse(first_value if "://" in first_value else f"https://bot.alazab.com{first_value}")
    path = parsed.path or "/"
    return "/" + path.strip("/") if path != "/" else "/"


def extract_request_site_host(request: Request) -> Optional[str]:
    for header_name in ("origin", "referer", "x-forwarded-host", "host"):
        hostname = extract_hostname(request.headers.get(header_name))
        if hostname and hostname != "bot.alazab.com":
            return hostname
    return extract_hostname(request.headers.get("host"))


def extract_request_site_path(request: Request) -> Optional[str]:
    for header_name in ("x-original-uri", "x-forwarded-uri", "referer"):
        path = extract_path(request.headers.get(header_name))
        if path and path not in {"/chat", "/chat/upload", "/chat/audio"}:
            return path
    return None


def is_internal_lead_notify_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except Exception:
        return False
    if parsed.path.rstrip("/") != "/lead":
        return False
    hostname = (parsed.hostname or "").lower()
    public_hostname = (urlparse(PUBLIC_BASE_URL).hostname or "").lower()
    internal_hosts = {"webhook", "localhost", "127.0.0.1", "0.0.0.0", public_hostname}
    return hostname in internal_hosts


# ══════════════════════════════════════════════════════════════
#  Brand Resolution
# ══════════════════════════════════════════════════════════════
def resolve_brand(
    explicit_brand: Optional[str],
    site_host: Optional[str],
    site_path: Optional[str],
    request: Request,
) -> str:
    normalized_brand = BRAND_ALIAS_MAP.get((explicit_brand or "").strip())
    if normalized_brand in BRAND_PROFILES:
        return normalized_brand

    for candidate_path in (
        site_path,
        extract_request_site_path(request),
        extract_path(request.headers.get("referer")),
    ):
        if candidate_path:
            brand = BRAND_PATH_MAP.get(candidate_path.rstrip("/") or "/")
            if brand:
                return brand

    for candidate in (
        site_host,
        extract_request_site_host(request),
        extract_hostname(request.headers.get("origin")),
        extract_hostname(request.headers.get("referer")),
    ):
        if candidate and candidate in SITE_BRAND_MAP:
            return SITE_BRAND_MAP[candidate]

    return os.getenv("DEFAULT_BRAND", "alazab_construction")


# ══════════════════════════════════════════════════════════════
#  Attachment / Message Serialization
# ══════════════════════════════════════════════════════════════
def serialize_attachment(attachment: dict[str, Any]) -> dict[str, Any]:
    serialized = {
        "id": attachment.get("id"),
        "kind": attachment.get("kind"),
        "name": attachment.get("name"),
        "size": attachment.get("size"),
        "content_type": attachment.get("content_type"),
        "download_url": f"/admin/uploads/{attachment['id']}/download" if attachment.get("id") else None,
    }
    if attachment.get("url"):
        serialized["url"] = attachment["url"]
    return serialized


def serialize_conversation_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    serialized_messages: list[dict[str, Any]] = []
    for message in messages:
        item = dict(message)
        attachments = item.get("attachments")
        if isinstance(attachments, list):
            item["attachments"] = [
                serialize_attachment(att) if isinstance(att, dict) else att
                for att in attachments
            ]
        serialized_messages.append(item)
    return serialized_messages


# ══════════════════════════════════════════════════════════════
#  Prompt Builders
# ══════════════════════════════════════════════════════════════
def build_file_prompt(
    attachment: dict[str, Any],
    brand: Optional[str],
    site_host: Optional[str],
    message: Optional[str] = None,
) -> str:
    user_note = f"رسالة المستخدم المصاحبة: {message.strip()}\n" if message and message.strip() else ""
    ref = attachment.get("url") or attachment.get("path") or attachment.get("relative_path") or attachment["name"]
    return (
        "قام المستخدم برفع ملف جديد داخل محادثة الموقع.\n"
        f"البراند: {brand or 'غير محدد'}\n"
        f"الموقع: {site_host or 'غير محدد'}\n"
        f"اسم الملف: {attachment['name']}\n"
        f"نوع الملف: {attachment['content_type']}\n"
        f"مرجع الملف: {ref}\n"
        f"{user_note}"
        "اشكر المستخدم وأخبره أن الملف وصل بنجاح، ثم اطلب منه أي تفاصيل إضافية يحتاجها."
    )


def build_audio_prompt(
    transcript: str,
    attachment: dict[str, Any],
    brand: Optional[str],
    site_host: Optional[str],
) -> str:
    ref = attachment.get("url") or attachment.get("path") or attachment.get("relative_path") or attachment["name"]
    return (
        "هذه رسالة صوتية من المستخدم بعد تفريغها إلى نص.\n"
        f"البراند: {brand or 'غير محدد'}\n"
        f"الموقع: {site_host or 'غير محدد'}\n"
        f"مرجع التسجيل: {ref}\n"
        f"النص المفرغ: {transcript}"
    )
