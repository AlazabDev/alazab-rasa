"""
webhook/auth.py — AzaBot Auth v4.1
====================================
✅ bcrypt بدل plain-text password
✅ كلمة مرور مستقلة لكل مستخدم
✅ جلسات Redis بدل ملف JSON
"""
from __future__ import annotations
import hashlib, hmac, json, logging, os, secrets, time
from typing import Optional
import bcrypt

logger = logging.getLogger("alazab.auth")

ADMIN_USERS: dict[str, dict] = {
    "admin@alazab.com":   {"name": "مدير النظام",     "role": "admin",  "avatar": "AD",  "_env_key": "ADMIN_PASSWORD_HASH_ADMIN"},
    "devops@alazab.com":  {"name": "DevOps",           "role": "devops", "avatar": "DV",  "_env_key": "ADMIN_PASSWORD_HASH_DEVOPS"},
    "ceo@alazab.com":     {"name": "المدير التنفيذي", "role": "ceo",    "avatar": "CEO", "_env_key": "ADMIN_PASSWORD_HASH_CEO"},
    "mohamed@alazab.com": {"name": "محمد",             "role": "admin",  "avatar": "MO",  "_env_key": "ADMIN_PASSWORD_HASH_MOHAMED"},
}

_SESSION_SECRET = os.getenv("ADMIN_SESSION_SECRET", "").strip()
_SESSION_TTL    = int(os.getenv("ADMIN_SESSION_TTL_SECONDS", str(7*24*3600)))

if not _SESSION_SECRET:
    import sys
    if os.getenv("NODE_ENV") == "production":
        raise RuntimeError("[FATAL] ADMIN_SESSION_SECRET غير مضبوط")
    _SESSION_SECRET = "dev-secret-not-for-production"
    print("[WARN] ADMIN_SESSION_SECRET غير مضبوط — وضع dev فقط", file=sys.stderr)

def _get_redis():
    import redis as _r
    return _r.Redis(
        host=os.getenv("REDIS_HOST","127.0.0.1"), port=int(os.getenv("REDIS_PORT","6379")),
        password=os.getenv("REDIS_PASSWORD") or None, db=int(os.getenv("REDIS_DB","0")),
        decode_responses=True, socket_connect_timeout=3, socket_timeout=3,
    )

_DUMMY_HASH = bcrypt.hashpw(b"dummy-timing-guard", bcrypt.gensalt(4))

def _get_user_hash(email: str) -> Optional[bytes]:
    user = ADMIN_USERS.get(email)
    if not user: return None
    stored = os.getenv(user["_env_key"], "").strip()
    if not stored:
        logger.warning("لم يُضبَط %s — المستخدم %s معطَّل", user["_env_key"], email)
        return None
    return stored.encode()

def verify_password(plain: str, email: str) -> bool:
    stored = _get_user_hash(email)
    if not stored:
        bcrypt.checkpw(b"dummy", _DUMMY_HASH)
        return False
    try:
        return bcrypt.checkpw(plain.strip().encode(), stored)
    except Exception:
        return False

def verify_user(email: str, password: str) -> Optional[dict]:
    email = email.strip().lower()
    is_valid = verify_password(password, email)
    if not is_valid or email not in ADMIN_USERS:
        return None
    u = ADMIN_USERS[email]
    return {"email": email, "name": u["name"], "role": u["role"], "avatar": u["avatar"]}

def _sign(token_id: str) -> str:
    sig = hmac.new(_SESSION_SECRET.encode(), token_id.encode(), hashlib.sha256).hexdigest()
    return f"{token_id}.{sig}"

def _unsign(token: str) -> Optional[str]:
    if "." not in token: return None
    token_id, sig = token.rsplit(".", 1)
    expected = hmac.new(_SESSION_SECRET.encode(), token_id.encode(), hashlib.sha256).hexdigest()
    return token_id if hmac.compare_digest(sig, expected) else None

def create_session(email: str) -> str:
    token_id = secrets.token_hex(32)
    now = int(time.time())
    data = json.dumps({"email": email, "created_at": now, "last_seen": now})
    try:
        _get_redis().setex(f"session:{token_id}", _SESSION_TTL, data)
    except Exception as exc:
        logger.error("Redis create_session failed: %s", exc)
        raise RuntimeError("تعذّر إنشاء الجلسة") from exc
    return _sign(token_id)

def verify_session(token: str) -> Optional[dict]:
    token_id = _unsign(token)
    if not token_id: return None
    try:
        r = _get_redis()
        raw = r.get(f"session:{token_id}")
        if not raw: return None
        session = json.loads(raw)
        now = int(time.time())
        if now - session.get("last_seen", 0) > 300:
            session["last_seen"] = now
            r.setex(f"session:{token_id}", _SESSION_TTL, json.dumps(session))
    except Exception as exc:
        logger.error("Redis verify_session failed: %s", exc)
        return None
    email = session.get("email", "")
    u = ADMIN_USERS.get(email)
    if not u: return None
    return {"email": email, "name": u["name"], "role": u["role"], "avatar": u["avatar"]}

def revoke_session(token: str) -> bool:
    token_id = _unsign(token)
    if not token_id: return False
    try:
        return bool(_get_redis().delete(f"session:{token_id}"))
    except Exception:
        return False

def list_active_sessions() -> list[dict]:
    try:
        r = _get_redis()
        out = []
        for k in r.keys("session:*"):
            raw = r.get(k)
            if raw:
                s = json.loads(raw)
                out.append({"email": s.get("email"), "created_at": s.get("created_at"),
                            "last_seen": s.get("last_seen"), "expires_in_seconds": r.ttl(k)})
        return out
    except Exception as exc:
        logger.error("Redis list_sessions failed: %s", exc)
        return []
