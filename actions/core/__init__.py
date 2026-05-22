"""
actions/core — طبقة المشتركات المركزية لـ AzaBot Actions
=========================================================

الوحدات:
  db.py        — Connection pool لـ PostgreSQL
  whatsapp.py  — إرسال رسائل WhatsApp
  gpt.py       — GPT client مع cache و rate limiting
"""
from .db import insert, fetch_one, fetch_all, acquire
from .whatsapp import send_text as send_whatsapp, send_notification
from .gpt import complete as gpt_complete, extract_json as gpt_extract_json

__all__ = [
    "insert",
    "fetch_one",
    "fetch_all",
    "acquire",
    "send_whatsapp",
    "send_notification",
    "gpt_complete",
    "gpt_extract_json",
]
