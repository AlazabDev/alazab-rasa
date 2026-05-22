"""
webhook/models.py — Pydantic Request/Response Models
=====================================================
كل المودلات الواردة والصادرة من الـ webhook.
"""
from __future__ import annotations

import re
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

_PHONE_RE = re.compile(r"^\+?[\d\s\-]{7,20}$")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

VALID_BRANDS = {
    "uberfix", "laban_alasfour", "alazab_construction",
    "luxury_finishing", "brand_identity",
}
VALID_CHANNELS = {"website", "whatsapp", "messenger", "telegram", "api"}


# ══════════════════════════════════════════════════════════════
#  Chat
# ══════════════════════════════════════════════════════════════

class ChatRequest(BaseModel):
    message:   str
    sender_id: str
    brand:     Optional[str] = None
    channel:   Optional[str] = "website"
    site_host: Optional[str] = None
    site_path: Optional[str] = None

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("الرسالة لا يمكن أن تكون فارغة")
        return v[:4000]  # حد أقصى 4000 حرف

    @field_validator("sender_id")
    @classmethod
    def sender_id_valid(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("sender_id مطلوب")
        return v[:128]

    @field_validator("brand")
    @classmethod
    def brand_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        normalized = v.strip().lower().replace("-", "_")
        return normalized  # نقبل أي قيمة ونطبّعها، التحقق الأعمق في action_session_start


class ChatResponse(BaseModel):
    responses:  list
    sender_id:  str
    channel:    str
    timestamp:  str
    attachment: Optional[dict[str, Any]] = None
    transcript: Optional[str] = None


class TTSRequest(BaseModel):
    text:  str
    voice: Optional[str] = None
    model: Optional[str] = None

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("text مطلوب")
        return v[:4000]


# ══════════════════════════════════════════════════════════════
#  Admin
# ══════════════════════════════════════════════════════════════

class AdminLoginRequest(BaseModel):
    email:    str
    password: str

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        v = v.strip().lower()
        if not v:
            raise ValueError("البريد الإلكتروني مطلوب")
        if not _EMAIL_RE.match(v):
            raise ValueError("صيغة البريد الإلكتروني غير صحيحة")
        return v

    @field_validator("password")
    @classmethod
    def password_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("كلمة المرور مطلوبة")
        return v


# ══════════════════════════════════════════════════════════════
#  Lead
# ══════════════════════════════════════════════════════════════

class LeadData(BaseModel):
    brand:           str
    user_name:       str
    user_phone:      str
    user_message:    str
    conversation_id: Optional[str] = None
    channel:         Optional[str] = "unknown"

    @field_validator("user_name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v or v == "غير محدد":
            raise ValueError("اسم العميل مطلوب")
        return v[:200]

    @field_validator("user_phone")
    @classmethod
    def phone_valid(cls, v: str) -> str:
        v = v.strip()
        if not v or v == "غير محدد":
            raise ValueError("رقم الهاتف مطلوب")
        if not _PHONE_RE.match(v):
            raise ValueError("صيغة رقم الهاتف غير صحيحة")
        return v


# ══════════════════════════════════════════════════════════════
#  UberFix Bot Gateway
# ══════════════════════════════════════════════════════════════

class BotGatewayRequest(BaseModel):
    action:     str
    payload:    dict[str, Any] = Field(default_factory=dict)
    session_id: Optional[str] = None
    metadata:   dict[str, Any] = Field(default_factory=dict)

    @field_validator("action")
    @classmethod
    def action_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("action مطلوب")
        return v

    @field_validator("session_id")
    @classmethod
    def session_id_clean(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return v.strip()[:128] or None
