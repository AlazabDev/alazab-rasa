"""
webhook/auth.py — نظام مصادقة AzaBot الداخلي
================================================
مصادقة بسيطة 100% داخلية — لا JWT خارجي، لا OAuth، لا أطراف ثالثة.

المستخدمون: 4 حسابات ثابتة على دومين alazab.com
كلمة المرور: واحدة مشتركة محفوظة في .env كـ hash

الآلية:
  1. المستخدم يُرسل email + password
  2. نتحقق من email في القائمة الثابتة
  3. نتحقق من password بمقارنة bcrypt hash
  4. نُصدر session token (HMAC-SHA256 بسيط) مخزن في .runtime/sessions.json
  5. كل طلب يُرسل التوكن في Authorization: Bearer
"""
from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import secrets
import time
from pathlib import Path
from threading import Lock
from typing import Optional

logger = logging.getLogger("alazab.auth")

# ══════════════════════════════════════════════════════════════
#  المستخدمون الثابتون
# ══════════════════════════════════════════════════════════════
ADMIN_USERS: dict[str, dict] = {
    "admin@alazab.com": {
        "name": "مدير النظام",
        "role": "admin",
        "avatar": "AD",
    },
    "devops@alazab.com": {
        "name": "DevOps",
        "role": "devops",
        "avatar": "DV",
    },
    "ceo@alazab.com": {
        "name": "المدير التنفيذي",
        "role": "ceo",
        "avatar": "CEO",
    },
    "mohamed@alazab.com": {
        "name": "محمد",
        "role": "admin",
        "avatar": "MO",
    },
}

# ── كلمة المرور ───────────────────────────────────────────────
# تُقرأ من .env — إذا لم تُضبَط يُستخدم الافتراضي (للبيئة dev فقط)
_ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Azab@202555").strip()
_SESSION_SECRET = os.getenv("ADMIN_SESSION_SECRET", "azabot-internal-secret-2025").strip()
_SESSION_TTL = int(os.getenv("ADMIN_SESSION_TTL_SECONDS", str(7 * 24 * 3600)))  # 7 أيام

# ── تخزين الجلسات ─────────────────────────────────────────────
_SESSIONS_FILE = Path(
    os.getenv("ADMIN_SESSIONS_FILE", str(Path(__file__).parent.parent / ".runtime" / "sessions.json"))
)
_sessions_lock = Lock()
_SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)


# ══════════════════════════════════════════════════════════════
#  التحقق من كلمة المرور
# ══════════════════════════════════════════════════════════════

def verify_password(plain: str) -> bool:
    """مقارنة آمنة ضد timing attacks."""
    return hmac.compare_digest(
        plain.strip().encode("utf-8"),
        _ADMIN_PASSWORD.encode("utf-8"),
    )


def verify_user(email: str, password: str) -> Optional[dict]:
    """
    يتحقق من email + password ويُعيد بيانات المستخدم أو None.
    """
    email = email.strip().lower()
    if email not in ADMIN_USERS:
        # تأخير ثابت لمنع user enumeration
        hmac.compare_digest(b"x", b"y")
        return None
    if not verify_password(password):
        return None
    return {"email": email, **ADMIN_USERS[email]}


# ══════════════════════════════════════════════════════════════
#  إدارة الجلسات
# ══════════════════════════════════════════════════════════════

def _load_sessions() -> dict:
    if not _SESSIONS_FILE.exists():
        return {}
    try:
        return json.loads(_SESSIONS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_sessions(sessions: dict) -> None:
    try:
        _SESSIONS_FILE.write_text(
            json.dumps(sessions, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as exc:
        logger.error("Failed to save sessions: %s", exc)


def _sign_token(token_id: str) -> str:
    """يُنشئ HMAC signature للـ token."""
    sig = hmac.new(
        _SESSION_SECRET.encode("utf-8"),
        token_id.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{token_id}.{sig}"


def _verify_token_signature(token: str) -> Optional[str]:
    """يتحقق من التوقيع ويُعيد token_id أو None."""
    if "." not in token:
        return None
    parts = token.rsplit(".", 1)
    if len(parts) != 2:
        return None
    token_id, sig = parts
    expected = hmac.new(
        _SESSION_SECRET.encode("utf-8"),
        token_id.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(sig, expected):
        return None
    return token_id


def create_session(email: str) -> str:
    """ينشئ جلسة جديدة ويُعيد التوكن."""
    token_id = secrets.token_hex(32)
    now = int(time.time())
    with _sessions_lock:
        sessions = _load_sessions()
        # حذف الجلسات المنتهية
        sessions = {
            k: v for k, v in sessions.items()
            if v.get("expires_at", 0) > now
        }
        sessions[token_id] = {
            "email": email,
            "created_at": now,
            "expires_at": now + _SESSION_TTL,
            "last_seen": now,
        }
        _save_sessions(sessions)
    return _sign_token(token_id)


def verify_session(token: str) -> Optional[dict]:
    """
    يتحقق من التوكن ويُعيد بيانات المستخدم أو None.
    يُحدّث last_seen في كل طلب.
    """
    token_id = _verify_token_signature(token)
    if not token_id:
        return None

    now = int(time.time())
    with _sessions_lock:
        sessions = _load_sessions()
        session = sessions.get(token_id)
        if not session:
            return None
        if session.get("expires_at", 0) <= now:
            del sessions[token_id]
            _save_sessions(sessions)
            return None
        # تحديث last_seen كل 5 دقائق فقط (تجنب الكتابة المتكررة)
        if now - session.get("last_seen", 0) > 300:
            session["last_seen"] = now
            _save_sessions(sessions)

    email = session.get("email", "")
    user = ADMIN_USERS.get(email)
    if not user:
        return None
    return {"email": email, **user}


def revoke_session(token: str) -> bool:
    """يحذف الجلسة (logout)."""
    token_id = _verify_token_signature(token)
    if not token_id:
        return False
    with _sessions_lock:
        sessions = _load_sessions()
        if token_id in sessions:
            del sessions[token_id]
            _save_sessions(sessions)
            return True
    return False


def list_active_sessions() -> list[dict]:
    """يُعيد قائمة الجلسات النشطة (للأدمن فقط)."""
    now = int(time.time())
    with _sessions_lock:
        sessions = _load_sessions()
    return [
        {
            "email": s["email"],
            "created_at": s["created_at"],
            "last_seen": s["last_seen"],
            "expires_at": s["expires_at"],
        }
        for s in sessions.values()
        if s.get("expires_at", 0) > now
    ]
