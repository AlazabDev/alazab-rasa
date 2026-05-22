"""
webhook/routers — FastAPI Routers
==================================
كل router معزول في ملفه الخاص:

  admin.py    — /admin/*
  chat.py     — /chat, /chat/upload, /chat/audio, /chat/tts
  channels.py — /webhook/meta, /webhook/telegram, /brands, /lead
"""
from .admin import router as admin_router
from .chat import router as chat_router
from .channels import router as channels_router

__all__ = ["admin_router", "chat_router", "channels_router"]
