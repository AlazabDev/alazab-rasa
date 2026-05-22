"""
webhook/services — Business Logic Services
==========================================
الطبقة الوسيطة بين الـ routers وقواعد البيانات/APIs الخارجية.

  admin_data.py    → حفظ/قراءة بيانات لوحة التحكم (JSON file)
  audio.py         → transcription + TTS عبر OpenAI
  channels.py      → إرسال عبر WhatsApp · Messenger · Telegram
  integrations.py  → محرك التكاملات الخارجية
  notifications.py → إشعارات leads لفريق المبيعات
  rasa_client.py   → تواصل مع Rasa Pro server
  uploads.py       → رفع وحفظ الملفات
"""
from . import admin_data
