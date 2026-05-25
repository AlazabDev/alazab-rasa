"""
webhook/routers/admin.py — Admin API v2
========================================
كل العمليات تمر على Supabase عبر services/admin_data.py
المصادقة عبر webhook/auth.py (HMAC داخلي)
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import time

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from ..auth import (
    ADMIN_USERS,
    create_session,
    list_active_sessions,
    revoke_session,
    verify_session,
    verify_user,
)
from ..config import UPLOADS_DIR
from ..models import AdminLoginRequest
from ..services.admin_data import (
    admin_stats_payload,
    load_settings, save_settings,
    list_conversations, get_conversation, delete_conversation,
    list_integrations, save_integration, delete_integration,
    list_integration_logs, save_integration_log,
    list_laban_orders, save_laban_order, delete_laban_order, update_laban_order_status,
    list_kb_collections, create_kb_collection, delete_kb_collection,
    list_kb_documents, delete_kb_document,
    list_training_jobs, save_training_job, delete_training_job,
    list_uploads, serialize_attachment, serialize_conversation_messages,
)
from ..services.integrations import test_integration
from ..utils import is_relative_to, jsonable

logger = logging.getLogger("alazab.admin")
router = APIRouter(prefix="/admin", tags=["Admin"])

# Rate limiter — Redis (مقاوم لإعادة التشغيل وmulti-process)
def _login_rate_check(ip: str) -> bool:
    """يُعيد True إذا كان مسموحاً بالمحاولة، False إذا تجاوز الحد."""
    try:
        import redis as _r, os, hashlib
        r = _r.Redis(
            host=os.getenv("REDIS_HOST", "127.0.0.1"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            password=os.getenv("REDIS_PASSWORD") or None,
            db=int(os.getenv("REDIS_DB", "0")),
            decode_responses=True,
            socket_connect_timeout=1, socket_timeout=1,
        )
        key = f"login_fail:{hashlib.md5(ip.encode(), usedforsecurity=False).hexdigest()[:12]}"
        count = r.get(key)
        return int(count or 0) < 10
    except Exception:
        return True  # Redis غير متاح — اسمح بالمحاولة

def _login_rate_record(ip: str) -> None:
    """يسجّل محاولة فاشلة."""
    try:
        import redis as _r, os, hashlib
        r = _r.Redis(
            host=os.getenv("REDIS_HOST", "127.0.0.1"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            password=os.getenv("REDIS_PASSWORD") or None,
            db=int(os.getenv("REDIS_DB", "0")),
            decode_responses=True,
            socket_connect_timeout=1, socket_timeout=1,
        )
        key = f"login_fail:{hashlib.md5(ip.encode(), usedforsecurity=False).hexdigest()[:12]}"
        pipe = r.pipeline()
        pipe.incr(key)
        pipe.expire(key, 300)
        pipe.execute()
    except Exception:
        pass

# ── Auth ──────────────────────────────────────────────────────

def _token(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:].strip()
    return request.cookies.get("azabot_admin_token", "").strip()

def _require_admin(request: Request) -> dict:
    user = verify_session(_token(request)) if _token(request) else None
    if not user:
        raise HTTPException(401, "يرجى تسجيل الدخول")
    return user

def _require_super(request: Request) -> dict:
    user = _require_admin(request)
    if user.get("role") not in ("admin", "devops"):
        raise HTTPException(403, "صلاحيات غير كافية")
    return user

# ── Auth Endpoints ────────────────────────────────────────────

@router.post("/login")
async def login(payload: AdminLoginRequest, request: Request):
    ip = request.client.host if request.client else "unknown"
    if not _login_rate_check(ip):
        raise HTTPException(429, "محاولات كثيرة — انتظر 5 دقائق")
    user = verify_user(payload.email, payload.password)
    if not user:
        _login_rate_record(ip)
        raise HTTPException(401, "البريد أو كلمة المرور غير صحيحة")
    token = create_session(user["email"])
    return {"token": token, "user": {"email": user["email"], "name": user["name"],
                                      "role": user["role"], "avatar": user["avatar"]}}

@router.post("/logout")
async def logout(request: Request):
    t = _token(request)
    if t: revoke_session(t)
    return {"ok": True}

@router.get("/me")
async def me(user: dict = Depends(_require_admin)):
    return user

@router.get("/users")
async def users(user: dict = Depends(_require_super)):
    return [{"email": e, **i} for e, i in ADMIN_USERS.items()]

@router.get("/sessions")
async def sessions(user: dict = Depends(_require_super)):
    return list_active_sessions()

# ── Main API ──────────────────────────────────────────────────

@router.api_route("/api", methods=["GET", "POST"])
async def api(request: Request, action: str,
              background_tasks: BackgroundTasks,
              user: dict = Depends(_require_admin)):
    body: dict[str, Any] = {}
    if request.method != "GET":
        try: body = await request.json()
        except Exception: body = {}
    result = await _dispatch(action, request, body, background_tasks)
    return JSONResponse(content=jsonable(result))

async def _dispatch(action: str, req: Request, body: dict, bg: BackgroundTasks) -> Any:
    qs = req.query_params

    # ── Stats & Settings ──────────────────────────────────────
    if action == "stats":
        return admin_stats_payload()

    if action == "get_settings":
        return load_settings()

    if action == "update_settings":
        save_settings(body)
        return load_settings()

    # ── Conversations ─────────────────────────────────────────
    if action == "list_conversations":
        return list_conversations(qs.get("q",""), qs.get("channel",""))

    if action == "get_conversation":
        conv = get_conversation(qs.get("id",""))
        if not conv: raise HTTPException(404, "المحادثة غير موجودة")
        conv["messages"] = serialize_conversation_messages(conv.get("messages",[]))
        return conv

    if action == "delete_conversation":
        delete_conversation(body.get("id",""))
        return {"ok": True}

    if action == "list_uploads":
        return [serialize_attachment(u) for u in list_uploads(qs.get("kind",""), qs.get("q",""))]

    # ── Integrations ──────────────────────────────────────────
    if action == "list_integrations":
        return list_integrations()

    if action == "save_integration":
        return save_integration(body)

    if action == "delete_integration":
        delete_integration(body.get("id",""))
        return {"ok": True}

    if action == "test_integration":
        int_id = body.get("id","")
        integrations = list_integrations()
        integration = next((i for i in integrations if i.get("id")==int_id), None)
        if not integration: raise HTTPException(404, "التكامل غير موجود")
        result = await test_integration(integration, {})
        # تسجيل النتيجة
        save_integration_log({
            "integration_id":   int_id,
            "integration_type": integration.get("type",""),
            "event":            "test",
            "status":           result.get("status","failed"),
            "created_at":       datetime.now(timezone.utc).isoformat(),
        })
        return result

    if action == "list_integration_logs":
        return list_integration_logs(100)

    # ── Laban Orders ──────────────────────────────────────────
    if action == "list_laban_orders":
        return list_laban_orders(qs.get("status",""), qs.get("q",""))

    if action == "save_laban_order":
        return save_laban_order(body)

    if action == "delete_laban_order":
        delete_laban_order(body.get("id",""))
        return {"ok": True}

    if action == "update_laban_order_status":
        update_laban_order_status(body.get("id",""), body.get("status",""))
        return {"ok": True}

    # ── Knowledge Base ────────────────────────────────────────
    if action == "list_kb_collections":
        return list_kb_collections()

    if action == "create_kb_collection":
        return create_kb_collection(body.get("name",""), body.get("description",""))

    if action == "delete_kb_collection":
        delete_kb_collection(body.get("id",""))
        return {"ok": True}

    if action == "list_kb_documents":
        return list_kb_documents(qs.get("collection_id",""), qs.get("q",""))

    if action == "upload_kb_documents":
        form = await req.form()
        col_id = str(form.get("collection_id","default"))
        urls = __import__("json").loads(str(form.get("urls","[]")))
        now = datetime.now(timezone.utc).isoformat()
        docs = []
        for f in form.getlist("files"):
            if not isinstance(f, UploadFile): continue
            doc = {"id": str(uuid.uuid4()), "collection_id": col_id,
                   "name": f.filename, "type": "file", "status": "ready", "created_at": now}
            docs.append(doc)
        for url in urls:
            docs.append({"id": str(uuid.uuid4()), "collection_id": col_id,
                         "name": url.split("/")[-1], "type": "url", "status": "ready", "created_at": now})
        return {"ok": True, "count": len(docs)}

    if action == "delete_kb_document":
        delete_kb_document(body.get("id",""))
        return {"ok": True}

    # ── Training ──────────────────────────────────────────────
    if action == "list_training_jobs":
        return list_training_jobs()

    if action == "start_training":
        form = await req.form()
        job = {
            "id": str(uuid.uuid4()),
            "name": str(form.get("name","training-new")),
            "model_type": str(form.get("model_type","rasa")),
            "status": "running",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        save_training_job(job)
        bg.add_task(_run_training, job["id"])
        return job

    if action == "delete_training_job":
        delete_training_job(body.get("id",""))
        return {"ok": True}

    raise HTTPException(400, f"إجراء غير مدعوم: {action}")


async def _run_training(job_id: str) -> None:
    import asyncio
    await asyncio.sleep(1)
    jobs = list_training_jobs()
    job = next((j for j in jobs if j.get("id")==job_id), None)
    if not job: return
    try:
        proc = await asyncio.create_subprocess_exec(
            "rasa", "train", "--fixed-model-name", f"model_{job_id[:8]}",
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        _, stderr = await asyncio.wait_for(proc.communicate(), timeout=600)
        job["status"] = "completed" if proc.returncode == 0 else "failed"
        if proc.returncode != 0:
            job["error"] = stderr.decode("utf-8","replace")[-300:]
    except Exception as exc:
        job["status"] = "failed"
        job["error"] = str(exc)
    finally:
        job["completed_at"] = datetime.now(timezone.utc).isoformat()
        save_training_job(job)

# ── Download ──────────────────────────────────────────────────

@router.get("/uploads/{upload_id}/download")
async def download(upload_id: str, user: dict = Depends(_require_admin)):
    uploads = list_uploads()
    upload = next((u for u in uploads if u.get("id")==upload_id), None)
    if not upload: raise HTTPException(404, "الملف غير موجود")
    file_path = Path(upload.get("path",""))
    if not file_path.exists() or not is_relative_to(file_path, UPLOADS_DIR):
        raise HTTPException(404, "الملف غير موجود على القرص")
    return FileResponse(str(file_path), filename=upload.get("name", file_path.name))

@router.get("/stats")
async def stats(user: dict = Depends(_require_admin)):
    return admin_stats_payload()
