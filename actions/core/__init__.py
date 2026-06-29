"""
actions/core — الطبقة المشتركة لـ AzaBot Actions
=================================================
db        → Supabase (قاعدة البيانات الموحدة)
gpt       → OpenAI GPT (cache + rate limit + retry)
whatsapp  → إرسال رسائل WhatsApp
"""
from .db import sb, insert, upsert, fetch_one, fetch_all, update, delete
from .whatsapp import send_text as send_whatsapp, send_notification
from .gpt import complete as gpt_complete, extract_json as gpt_extract_json

__all__ = [
    # DB
    "sb", "insert", "upsert", "fetch_one", "fetch_all", "update", "delete",
    # WhatsApp
    "send_whatsapp", "send_notification",
    # GPT
    "gpt_complete", "gpt_extract_json",
]
