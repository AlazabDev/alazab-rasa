"""
webhook/models.py — Pydantic Request/Response Models
=====================================================
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


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
        if not v.strip():
            raise ValueError("الرسالة لا يمكن أن تكون فارغة")
        return v.strip()


class AdminLoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def email_not_empty(cls, value: str) -> str:
        email = value.strip().lower()
        if not email:
            raise ValueError("البريد الإلكتروني مطلوب")
        return email

    @field_validator("password")
    @classmethod
    def password_not_empty(cls, value: str) -> str:
        password = value.strip()
        if not password:
            raise ValueError("كلمة المرور مطلوبة")
        return password


class LeadData(BaseModel):
    brand:           str
    user_name:       str
    user_phone:      str
    user_message:    str
    conversation_id: Optional[str] = None
    channel:         Optional[str] = "unknown"


class ChatResponse(BaseModel):
    responses:  list
    sender_id:  str
    channel:    str
    timestamp:  str
    attachment: Optional[dict[str, Any]] = None
    transcript: Optional[str] = None


class TTSRequest(BaseModel):
    text: str
    voice: Optional[str] = None
    model: Optional[str] = None

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        value = v.strip()
        if not value:
            raise ValueError("text مطلوب")
        return value[:4000]


class BotGatewayRequest(BaseModel):
    action: str
    payload: dict[str, Any] = Field(default_factory=dict)
    session_id: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("action")
    @classmethod
    def action_not_empty(cls, value: str) -> str:
        action = value.strip()
        if not action:
            raise ValueError("action مطلوب")
        return action
