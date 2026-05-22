"""
webhook/routers/admin.py — Admin API Router v2
================================================
مصادقة داخلية بالكامل عبر webhook/auth.py
4 مستخدمين ثابتين — لا JWT خارجي — لا أطراف ثالثة
"""
from __future__ import annotations

import json
import logging
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
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
    load_admin_data,
    save_admin_data,
)
from ..services.integrations import test_integration
from ..utils import is_relative_to, jsonable, serialize_attachment, serialize_conversation_messages

logger = logging.getLogger("alazab.webhook.admin")

router = APIRouter(prefix="/admin", tags=["Admin"])

# ── Rate Limiter ─────────────────────────────────────────────
_login_attempts: dict[str, list[float]] = defaultdict(list)
_LOGIN_MAX   = 10
_LOGIN_WIN   = 300   # 5 دقائق


# ══════════════════════════════════════════════════════════════
#  Auth Dependency
# ══════════════════════════════════════════════════════════════

def _get_token(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:].strip()
    # دعم cookie أيضاً
    return request.cookies.get("azabot_admin_token", "").strip()


def _require_admin(request: Request) -> dict:
    """يُعيد بيانات المستخدم أو يرفع 401."""
    token = _get_token(request)
    user = verify_session(token) if token else None
    if not user:
        raise HTTPException(status_code=401, detail="يرجى تسجيل الدخول")
    return user


def _require_super_admin(request: Request) -> dict:
    """admin أو devops فقط."""
    user = _require_admin(request)
    if user.get("role") not in ("admin", "devops"):
        raise HTTPException(status_code=403, detail="صلاحيات غير كافية")
    return user


# ══════════════════════════════════════════════════════════════
#  Auth Endpoints
# ══════════════════════════════════════════════════════════════

@router.post("/login")
async def admin_login(payload: AdminLoginRequest, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    # Rate limit
    _login_attempts[client_ip] = [t for t in _login_attempts[client_ip] if now - t < _LOGIN_WIN]
    if len(_login_attempts[client_ip]) >= _LOGIN_MAX:
        raise HTTPException(status_code=429, detail="محاولات كثيرة — انتظر 5 دقائق")

    user = verify_user(payload.email, payload.password)
    if not user:
        _login_attempts[client_ip].append(now)
        logger.warning("Failed login attempt: %s from %s", payload.email, client_ip)
        raise HTTPException(status_code=401, detail="البريد الإلكتروني أو كلمة المرور غير صحيحة")

    token = create_session(user["email"])
    logger.info("Admin login: %s from %s", user["email"], client_ip)
    return {
        "token": token,
        "user": {
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
            "avatar": user["avatar"],
        },
    }


@router.post("/logout")
async def admin_logout(request: Request):
    token = _get_token(request)
    if token:
        revoke_session(token)
    return {"ok": True}


@router.get("/me")
async def admin_me(user: dict = Depends(_require_admin)):
    return user


@router.get("/users")
async def admin_users(user: dict = Depends(_require_super_admin)):
    """قائمة المستخدمين المسموح لهم."""
    return [
        {"email": email, **info}
        for email, info in ADMIN_USERS.items()
    ]


@router.get("/sessions")
async def admin_sessions(user: dict = Depends(_require_super_admin)):
    """الجلسات النشطة حالياً."""
    return list_active_sessions()


# ══════════════════════════════════════════════════════════════
#  System Endpoints
# ══════════════════════════════════════════════════════════════

@router.get("/stats")
async def admin_stats(user: dict = Depends(_require_admin)):
    return admin_stats_payload()


@router.get("/uploads/{upload_id}/download")
async def admin_download_upload(upload_id: str, user: dict = Depends(_require_admin)):
    data = load_admin_data()
    upload = next((u for u in data.get("uploads", []) if u.get("id") == upload_id), None)
    if not upload:
        raise HTTPException(status_code=404, detail="الملف غير موجود")
    file_path = Path(upload.get("path", ""))
    if not file_path.exists() or not is_relative_to(file_path, UPLOADS_DIR):
        raise HTTPException(status_code=404, detail="الملف غير موجود على القرص")
    return FileResponse(
        path=str(file_path),
        filename=upload.get("name", file_path.name),
        media_type=upload.get("content_type", "application/octet-stream"),
    )


# ══════════════════════════════════════════════════════════════
#  Admin API (الموزّع)
# ══════════════════════════════════════════════════════════════

@router.api_route("/api", methods=["GET", "POST"])
async def admin_api(
    request: Request,
    action: str,
    background_tasks: BackgroundTasks,
    user: dict = Depends(_require_admin),
):
    data = load_admin_data()
    body: dict[str, Any] = {}
    if request.method != "GET":
        try:
            parsed = await request.json()
            if isinstance(parsed, dict):
                body = parsed
        except Exception:
            body = {}

    result = await _handle_admin_action(action, request, body, data, background_tasks, user)
    return JSONResponse(content=jsonable(result))


async def _handle_admin_action(
    action: str,
    request: Request,
    body: dict[str, Any],
    data: dict[str, Any],
    bg: BackgroundTasks,
    user: dict,
) -> Any:
    handlers = {
        "stats": _action_stats,
        "get_settings": _action_get_settings,
        "update_settings": _action_update_settings,
        "list_conversations": _action_list_conversations,
        "list_uploads": _action_list_uploads,
        "get_conversation": _action_get_conversation,
        "delete_conversation": _action_delete_conversation,
        "list_integrations": _action_list_integrations,
        "save_integration": _action_save_integration,
        "delete_integration": _action_delete_integration,
        "test_integration": _action_test_integration,
        "list_integration_logs": _action_list_integration_logs,
        "list_kb_collections": _action_list_kb_collections,
        "create_kb_collection": _action_create_kb_collection,
        "delete_kb_collection": _action_delete_kb_collection,
        "list_kb_documents": _action_list_kb_documents,
        "upload_kb_documents": _action_upload_kb_documents,
        "delete_kb_document": _action_delete_kb_document,
        "list_training_jobs": _action_list_training_jobs,
        "start_training": _action_start_training,
        "delete_training_job": _action_delete_training_job,
        # Laban Alasfour — نموذج طلبات التصنيع
        "list_laban_orders": _action_list_laban_orders,
        "save_laban_order": _action_save_laban_order,
        "delete_laban_order": _action_delete_laban_order,
        "update_laban_order_status": _action_update_laban_order_status,
    }
    handler = handlers.get(action)
    if handler is None:
        raise HTTPException(status_code=400, detail=f"إجراء غير مدعوم: {action}")
    return await handler(request, body, data, bg)


# ── Stats & Settings ──────────────────────────────────────────
async def _action_stats(r, b, d, bg): return admin_stats_payload()
async def _action_get_settings(r, b, d, bg): return d.get("settings", {})
async def _action_update_settings(r, b, d, bg):
    d["settings"] = {**d.get("settings", {}), **b}
    save_admin_data(d); return d["settings"]

# ── Conversations ─────────────────────────────────────────────
async def _action_list_conversations(r, b, d, bg):
    q = (r.query_params.get("q") or "").lower()
    convs = d.get("conversations", [])
    if q:
        convs = [c for c in convs if q in str(c.get("session_id","")).lower()
                 or q in str(c.get("brand","")).lower()
                 or q in str(c.get("channel","")).lower()]
    return [{"id":c.get("id"),"session_id":c.get("session_id"),
             "brand":c.get("brand"),"channel":c.get("channel"),
             "message_count":len(c.get("messages",[])),"last_message_at":c.get("last_message_at") or c.get("created_at")}
            for c in convs]

async def _action_list_uploads(r, b, d, bg):
    q = (r.query_params.get("q") or "").lower()
    kind = (r.query_params.get("kind") or "").lower()
    uploads = d.get("uploads", [])
    if kind: uploads = [u for u in uploads if str(u.get("kind","")).lower()==kind]
    if q: uploads = [u for u in uploads if q in str(u.get("name","")).lower() or q in str(u.get("session_id","")).lower()]
    return [serialize_attachment(u) for u in uploads[:500]]

async def _action_get_conversation(r, b, d, bg):
    conv_id = r.query_params.get("id")
    conv = next((c for c in d.get("conversations",[]) if c.get("id")==conv_id), None)
    if not conv: raise HTTPException(404,"المحادثة غير موجودة")
    return {**conv,"messages":serialize_conversation_messages(conv.get("messages",[]))}

async def _action_delete_conversation(r, b, d, bg):
    d["conversations"] = [c for c in d.get("conversations",[]) if c.get("id")!=b.get("id")]
    save_admin_data(d); return {"ok":True}

# ── Integrations ──────────────────────────────────────────────
async def _action_list_integrations(r, b, d, bg): return d.get("integrations",[])
async def _action_save_integration(r, b, d, bg):
    integrations = d.setdefault("integrations",[])
    item = dict(b)
    if not item.get("id"):
        item["id"] = str(uuid.uuid4())
        item["created_at"] = datetime.now(timezone.utc).isoformat()
        integrations.insert(0,item)
    else:
        integrations[:] = [{**old,**item} if old.get("id")==item["id"] else old for old in integrations]
    save_admin_data(d); return item

async def _action_delete_integration(r, b, d, bg):
    d["integrations"] = [i for i in d.get("integrations",[]) if i.get("id")!=b.get("id")]
    save_admin_data(d); return {"ok":True}

async def _action_test_integration(r, b, d, bg):
    integration = next((i for i in d.get("integrations",[]) if i.get("id")==b.get("id")),None)
    if not integration: raise HTTPException(404,"التكامل غير موجود")
    return await test_integration(integration, d)

async def _action_list_integration_logs(r, b, d, bg):
    return d.get("logs", [])[:100]

# ── Knowledge Base ─────────────────────────────────────────────
async def _action_list_kb_collections(r, b, d, bg): return d.get("kb_collections",[])
async def _action_create_kb_collection(r, b, d, bg):
    col = {"id":str(uuid.uuid4()),"name":b.get("name","بدون اسم"),"description":b.get("description",""),
           "document_count":0,"chunk_count":0,"created_at":datetime.now(timezone.utc).isoformat()}
    d.setdefault("kb_collections",[]).append(col); save_admin_data(d); return col

async def _action_delete_kb_collection(r, b, d, bg):
    col_id = b.get("id")
    d["kb_collections"] = [c for c in d.get("kb_collections",[]) if c["id"]!=col_id]
    d["kb_documents"] = [doc for doc in d.get("kb_documents",[]) if doc["collection_id"]!=col_id]
    save_admin_data(d); return {"ok":True}

async def _action_list_kb_documents(r, b, d, bg):
    col_id = r.query_params.get("collection_id")
    q = (r.query_params.get("q") or "").lower()
    docs = d.get("kb_documents",[])
    if col_id: docs = [doc for doc in docs if doc.get("collection_id")==col_id]
    if q: docs = [doc for doc in docs if q in doc.get("name","").lower()]
    return docs

async def _action_upload_kb_documents(r, b, d, bg):
    form = await r.form()
    col_id = str(form.get("collection_id","default"))
    files = form.getlist("files"); urls = json.loads(str(form.get("urls","[]")))
    new_docs = []; now = datetime.now(timezone.utc).isoformat()
    for f in files:
        if not isinstance(f, UploadFile): continue
        doc_id = str(uuid.uuid4())
        dest = UPLOADS_DIR / "kb" / doc_id / (f.filename or "upload.bin")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(await f.read())
        new_docs.append({"id":doc_id,"collection_id":col_id,"name":f.filename,"type":"file","status":"ready","created_at":now,"metadata":{"source":f.filename}})
    for url in urls:
        new_docs.append({"id":str(uuid.uuid4()),"collection_id":col_id,"name":url.split("/")[-1] or url,"type":"url","status":"ready","created_at":now,"metadata":{"source":url}})
    d.setdefault("kb_documents",[]).extend(new_docs)
    for col in d.get("kb_collections",[]):
        if col["id"]==col_id: col["document_count"]=sum(1 for doc in d["kb_documents"] if doc["collection_id"]==col_id)
    save_admin_data(d); return {"ok":True,"count":len(new_docs)}

async def _action_delete_kb_document(r, b, d, bg):
    d["kb_documents"] = [doc for doc in d.get("kb_documents",[]) if doc["id"]!=b.get("id")]
    save_admin_data(d); return {"ok":True}

# ── Training ──────────────────────────────────────────────────
async def _action_list_training_jobs(r, b, d, bg): return d.get("training_jobs",[])
async def _action_start_training(r, b, d, bg):
    form = await r.form()
    job_id = str(uuid.uuid4())
    job = {"id":job_id,"name":str(form.get("name","تدريب جديد")),"model_type":str(form.get("model_type","rasa")),
           "status":"running","created_at":datetime.now(timezone.utc).isoformat(),"files":[],"stats":{"epochs":0,"accuracy":0}}
    d.setdefault("training_jobs",[]).insert(0,job); save_admin_data(d)
    bg.add_task(_run_training_bg, job_id); return job

async def _action_delete_training_job(r, b, d, bg):
    d["training_jobs"] = [j for j in d.get("training_jobs",[]) if j["id"]!=b.get("id")]
    save_admin_data(d); return {"ok":True}

# ── Laban Alasfour Orders ─────────────────────────────────────
async def _action_list_laban_orders(r, b, d, bg):
    q = (r.query_params.get("q") or "").lower()
    status = r.query_params.get("status","")
    orders = d.get("laban_orders", [])
    if status: orders = [o for o in orders if o.get("status")==status]
    if q: orders = [o for o in orders if q in str(o.get("client_name","")).lower()
                    or q in str(o.get("phone","")).lower()
                    or q in str(o.get("order_number","")).lower()]
    return orders

async def _action_save_laban_order(r, b, d, bg):
    orders = d.setdefault("laban_orders", [])
    now = datetime.now(timezone.utc).isoformat()
    order = dict(b)
    if not order.get("id"):
        # توليد رقم طلب تسلسلي
        count = len(orders) + 1
        order["id"] = str(uuid.uuid4())
        order["order_number"] = f"LBN-{datetime.now(timezone.utc).strftime('%Y%m')}-{count:04d}"
        order["created_at"] = now
        order["status"] = order.get("status", "new")
        orders.insert(0, order)
    else:
        orders[:] = [{**old, **order, "updated_at": now} if old.get("id")==order["id"] else old for old in orders]
    save_admin_data(d)
    return order

async def _action_delete_laban_order(r, b, d, bg):
    d["laban_orders"] = [o for o in d.get("laban_orders",[]) if o.get("id")!=b.get("id")]
    save_admin_data(d); return {"ok":True}

async def _action_update_laban_order_status(r, b, d, bg):
    order_id = b.get("id"); new_status = b.get("status")
    for o in d.get("laban_orders",[]):
        if o.get("id")==order_id:
            o["status"] = new_status
            o["updated_at"] = datetime.now(timezone.utc).isoformat()
            break
    save_admin_data(d); return {"ok":True}


# ── Training Background ───────────────────────────────────────
async def _run_training_bg(job_id: str) -> None:
    import asyncio
    from ..services.admin_data import load_admin_data, save_admin_data as _save
    await asyncio.sleep(1)
    data = load_admin_data()
    job = next((j for j in data.get("training_jobs",[]) if j["id"]==job_id), None)
    if not job: return
    try:
        proc = await asyncio.create_subprocess_exec(
            "rasa","train","--fixed-model-name",f"model_{job_id[:8]}",
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        _, stderr = await asyncio.wait_for(proc.communicate(), timeout=600)
        job["status"] = "completed" if proc.returncode==0 else "failed"
        if proc.returncode != 0: job["error"] = stderr.decode("utf-8","replace")[-500:]
    except Exception as exc:
        job["status"] = "failed"; job["error"] = str(exc)
    finally:
        job["completed_at"] = datetime.now(timezone.utc).isoformat()
        _save(data)
