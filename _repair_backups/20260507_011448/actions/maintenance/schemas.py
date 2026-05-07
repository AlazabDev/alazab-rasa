"""Data normalization for maintenance requests."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional
from urllib.parse import quote

from .errors import MaintenanceValidationError


SERVICE_KEYWORDS = {
    "electrical": ("كهرب", "نور", "قاطع", "ماس", "electric", "power"),
    "plumbing": ("سباك", "مياه", "تسريب", "صرف", "plumb", "water"),
    "ac": ("تكييف", "تكيف", "تبريد", "ac", "air"),
    "painting": ("دهان", "نقاشة", "paint"),
    "carpentry": ("نجار", "باب", "خشب", "carp"),
    "cleaning": ("نظافة", "تنظيف", "clean"),
}

HIGH_PRIORITY_KEYWORDS = (
    "عاجل",
    "طارئ",
    "خطر",
    "ماس",
    "حريق",
    "تسريب شديد",
    "emergency",
    "urgent",
    "high",
)


@dataclass(frozen=True)
class MaintenanceTicket:
    request_number: str
    request_id: str
    track_url: str
    message: str = ""

    @property
    def display_number(self) -> str:
        return self.request_number or self.request_id


@dataclass(frozen=True)
class MaintenanceRequest:
    client_name: str
    client_phone: str
    description: str
    service_type: str
    priority: str
    title: str
    location: str
    session_id: str
    idempotency_key: str
    channel: str = "bot_gateway"


def build_create_request(
    *,
    client_name: Optional[str],
    client_phone: Optional[str],
    description: Optional[str],
    tracker_sender_id: Optional[str],
) -> MaintenanceRequest:
    name = clean_text(client_name) or "عميل UberFix"
    phone = normalize_phone(client_phone)
    desc = clean_text(description)

    missing = []
    if not phone:
        missing.append("phone")
    if not desc:
        missing.append("description")
    if missing:
        raise MaintenanceValidationError(missing)

    service_type = infer_service_type(desc)
    priority = infer_priority(desc)
    location = infer_location(desc)
    session_id = clean_text(tracker_sender_id) or session_id_from_phone(phone)
    idempotency_key = build_idempotency_key(phone, service_type, desc)

    return MaintenanceRequest(
        client_name=name[:120],
        client_phone=phone,
        description=desc[:1000],
        service_type=service_type,
        priority=priority,
        title=infer_title(desc),
        location=location,
        session_id=session_id,
        idempotency_key=idempotency_key,
    )


def normalize_ticket(data: dict[str, Any], track_base_url: str) -> MaintenanceTicket:
    result = data.get("data") if isinstance(data.get("data"), dict) else {}
    request_number = clean_text(
        data.get("request_number")
        or data.get("tracking_number")
        or result.get("request_number")
        or result.get("tracking_number")
    )
    request_id = clean_text(
        data.get("request_id")
        or result.get("request_id")
        or result.get("id")
    )
    track_url = clean_text(data.get("track_url") or result.get("track_url"))
    if not track_url:
        track_url = build_track_url(track_base_url, request_id or request_number)
    return MaintenanceTicket(
        request_number=request_number,
        request_id=request_id,
        track_url=track_url,
        message=clean_text(data.get("message") or result.get("message")),
    )


def extract_request_number(text: str) -> str:
    patterns = [
        r"\b([A-Z]{2,4}-[A-Z]{2,4}-\d{2}-\d{2}-\d{4,8})\b",
        r"\b([A-Z]{2,4}-\d{2,4}-\d{2,4}-\d{4,8})\b",
        r"\b([A-Z]{2,4}-\d{2,4}-\d{4,8})\b",
        r"\b([A-Z]{2,4}-?\d{5,12})\b",
        r"\b([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})\b",
        r"\b(\d{5,10})\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text or "", flags=re.IGNORECASE)
        if match:
            return match.group(1).strip().upper()
    return ""


def clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_phone(value: Any) -> str:
    raw = str(value or "").strip()
    digits = re.sub(r"\D+", "", raw)
    if digits.startswith("20") and len(digits) == 12:
        digits = "0" + digits[2:]
    if len(digits) == 10 and digits.startswith("1"):
        digits = "0" + digits
    if re.fullmatch(r"01[0125]\d{8}", digits):
        return digits
    return ""


def infer_service_type(description: str) -> str:
    text = description.lower()
    for service_type, keywords in SERVICE_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return service_type
    return "general"


def infer_priority(description: str) -> str:
    text = description.lower()
    return "high" if any(keyword in text for keyword in HIGH_PRIORITY_KEYWORDS) else "normal"


def infer_title(description: str) -> str:
    text = clean_text(description)
    return (text[:80] if text else "طلب صيانة من عزبوت")


def infer_location(description: str) -> str:
    text = clean_text(description)
    patterns = [
        r"(?:فرع|محل|موقع)\s+([^،,.؛\n]{2,80})",
        r"(?:في|بـ|ب)\s+([^،,.؛\n]{2,80})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return clean_text(match.group(1))[:120]
    return "غير محدد"


def session_id_from_phone(phone: str) -> str:
    digits = re.sub(r"\D+", "", phone or "")
    return f"azabot_{digits[-11:]}" if digits else "azabot_web"


def build_idempotency_key(phone: str, service_type: str, description: str) -> str:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    normalized_description = clean_text(description).lower()[:160]
    raw = "|".join([day, phone, service_type, normalized_description])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build_track_url(track_base_url: str, order_id: str) -> str:
    base = (track_base_url or "").rstrip("/")
    return f"{base}/{quote(order_id, safe='')}" if base and order_id else ""
