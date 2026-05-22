"""
webhook/_uberfix_gateway.py — UberFix Bot-Gateway Engine
=========================================================
محرك بوابة UberFix المحلي.

[مُستخرَج من server.py — كان 1164 سطر مدفون في المنتصف]

يُستدعى من:
  server.py → POST /uberfix/bot-gateway

الوظيفة:
  يستقبل طلبات من Rasa Actions عبر واجهة bot-gateway
  ويُنفّذها مباشرة على قاعدة بيانات PostgreSQL.
"""
from __future__ import annotations

import logging
import os
import time
from typing import Any, Optional

from fastapi import HTTPException

from .config import (
    DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER,
    UBERFIX_API_KEY, UBERFIX_TRACK_BASE_URL,
    UBERFIX_SERVICE_TYPES,
)

logger = logging.getLogger("alazab.webhook.uberfix_gateway")

def _uberfix_db_connect():
    if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
        raise HTTPException(status_code=503, detail="PostgreSQL غير مضبوط في .env")

    import psycopg
    from psycopg.rows import dict_row

    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            return psycopg.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                connect_timeout=5,
                row_factory=dict_row,
            )
        except Exception as exc:
            if attempt < max_retries - 1:
                logger.warning(
                    "UberFix PostgreSQL connection attempt %d failed: %s. Retrying in %ds...",
                    attempt + 1,
                    exc,
                    retry_delay,
                )
                time.sleep(retry_delay)
            else:
                logger.error(
                    "UberFix PostgreSQL connection failed after %d attempts: %s",
                    max_retries,
                    exc,
                )
                raise HTTPException(
                    status_code=503, detail="PostgreSQL غير متاح لبوابة UberFix"
                )


def _authenticate_uberfix_gateway(
    cur, request_context: dict[str, Any]
) -> dict[str, Any]:
    api_key = _extract_gateway_api_key(request_context)
    if not api_key:
        raise HTTPException(status_code=401, detail="مفتاح API مطلوب")

    cur.execute(
        """
        SELECT id, name, rate_limit_per_minute, allowed_origins
        FROM api_consumers
        WHERE is_active = true
          AND (
            api_key = %s
            OR api_key_hash = encode(digest(%s, 'sha256'), 'hex')
          )
        LIMIT 1
        """,
        (api_key, api_key),
    )
    consumer = cur.fetchone()
    if consumer:
        _verify_gateway_origin(consumer, request_context)
        return consumer

    if UBERFIX_API_KEY and hmac.compare_digest(api_key, UBERFIX_API_KEY):
        return {
            "id": None,
            "name": "env:azabot",
            "rate_limit_per_minute": 60,
            "allowed_origins": [],
        }

    raise HTTPException(status_code=401, detail="مفتاح API غير صالح")


def _extract_gateway_api_key(request_context: dict[str, Any]) -> str:
    api_key = str(request_context.get("x_api_key") or "").strip()
    if api_key:
        return api_key

    auth_header = str(request_context.get("authorization") or "").strip()
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:].strip()
    return ""


def _verify_gateway_origin(
    consumer: dict[str, Any], request_context: dict[str, Any]
) -> None:
    allowed = consumer.get("allowed_origins") or []
    origin = str(request_context.get("origin") or "").strip().rstrip("/")
    if not origin or not allowed:
        return
    normalized = {
        str(item).strip().rstrip("/") for item in allowed if str(item).strip()
    }
    if "*" in normalized or origin in normalized:
        return
    raise HTTPException(status_code=403, detail="Origin غير مسموح لهذا المفتاح")


def _enforce_uberfix_rate_limit(cur, consumer: dict[str, Any]) -> None:
    consumer_id = consumer.get("id")
    if not consumer_id:
        return
    limit = int(consumer.get("rate_limit_per_minute") or 60)
    cur.execute(
        """
        SELECT count(*) AS total
        FROM api_gateway_logs
        WHERE consumer_id = %s
          AND created_at >= now() - interval '1 minute'
        """,
        (consumer_id,),
    )
    row = cur.fetchone() or {}
    if int(row.get("total") or 0) >= limit:
        raise HTTPException(
            status_code=429, detail="تم تجاوز حد الطلبات، حاول بعد دقيقة"
        )


def _execute_uberfix_action(
    cur,
    action: str,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    handlers = {
        "create_request": _uberfix_create_request,
        "check_status": _uberfix_check_status,
        "get_request_details": _uberfix_get_request_details,
        "update_request": _uberfix_update_request,
        "cancel_request": _uberfix_cancel_request,
        "add_note": _uberfix_add_note,
        "assign_technician": _uberfix_assign_technician,
        "list_technicians": _uberfix_list_technicians,
        "list_categories": _uberfix_list_categories,
        "list_services": _uberfix_list_services,
        "get_branches": _uberfix_get_branches,
        "find_nearest_branch": _uberfix_find_nearest_branch,
        "collect_customer_info": _uberfix_collect_customer_info,
        "get_quote": _uberfix_get_quote,
        "get_status": _uberfix_get_status,
        "transition_stage": _uberfix_transition_stage,
    }
    handler = handlers.get(action)
    if not handler:
        raise HTTPException(status_code=400, detail=f"عملية غير مدعومة: {action}")
    return handler(cur, payload, session_id, metadata)


def _uberfix_create_request(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    client_name = _require_payload_text(payload, "client_name", "اسم العميل مطلوب", 120)
    client_phone = _require_payload_text(
        payload, "client_phone", "رقم هاتف العميل مطلوب", 40
    )
    description = _require_payload_text(
        payload, "description", "وصف المشكلة مطلوب", 1000
    )
    service_type = _safe_gateway_text(payload.get("service_type") or "general", 60)
    priority = _safe_gateway_text(payload.get("priority") or "medium", 20)
    if priority not in {"low", "medium", "normal", "high"}:
        priority = "medium"

    request_metadata = dict(metadata)
    if isinstance(payload.get("metadata"), dict):
        request_metadata.update(payload["metadata"])

    from psycopg.types.json import Jsonb

    cur.execute(
        """
        INSERT INTO maintenance_requests (
            channel, session_id, client_name, client_phone, client_email,
            location, service_type, title, description, priority,
            latitude, longitude, metadata
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *
        """,
        (
            _safe_gateway_text(
                payload.get("channel") or metadata.get("source") or "bot_gateway", 80
            ),
            session_id,
            client_name,
            client_phone,
            _safe_gateway_text(payload.get("client_email"), 180) or None,
            _safe_gateway_text(payload.get("location"), 300) or "غير محدد",
            service_type,
            _safe_gateway_text(payload.get("title"), 200) or description[:120],
            description,
            priority,
            _numeric_or_none(payload.get("latitude")),
            _numeric_or_none(payload.get("longitude")),
            Jsonb(request_metadata),
        ),
    )
    row = cur.fetchone()
    tracking_reference = row.get("request_number") or str(row["id"])
    track_url = f"{UBERFIX_TRACK_BASE_URL}/{tracking_reference}"
    cur.execute(
        "UPDATE maintenance_requests SET track_url = %s WHERE id = %s RETURNING *",
        (track_url, row["id"]),
    )
    row = cur.fetchone()

    _insert_uberfix_audit(
        cur,
        "BOT_CREATE_REQUEST",
        "maintenance_request",
        row["id"],
        None,
        row,
        {"session_id": session_id, "source": metadata.get("source")},
    )

    return {
        "success": True,
        "message": f"تم إنشاء الطلب بنجاح. رقم التتبع: {row['request_number']}",
        "request_id": str(row["id"]),
        "request_number": row["request_number"],
        "tracking_number": row["request_number"],
        "track_url": row["track_url"],
        "data": _maintenance_request_public(row),
    }


def _uberfix_check_status(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    search_term = _safe_gateway_text(
        payload.get("search_term")
        or payload.get("request_number")
        or payload.get("client_phone")
        or "",
        120,
    )
    search_type = _safe_gateway_text(payload.get("search_type") or "request_number", 40)
    if not search_term:
        raise HTTPException(status_code=400, detail="قيمة البحث مطلوبة")

    if search_type == "phone":
        digits = _phone_digits(search_term)[-9:]
        cur.execute(
            """
            SELECT *
            FROM maintenance_requests
            WHERE regexp_replace(coalesce(client_phone, ''), '\\D', '', 'g') LIKE %s
            ORDER BY created_at DESC
            LIMIT 5
            """,
            (f"%{digits}",),
        )
    elif search_type == "name":
        cur.execute(
            """
            SELECT *
            FROM maintenance_requests
            WHERE client_name ILIKE %s
            ORDER BY created_at DESC
            LIMIT 5
            """,
            (f"%{search_term}%",),
        )
    else:
        cur.execute(
            """
            SELECT *
            FROM maintenance_requests
            WHERE upper(request_number) = upper(%s)
               OR id::text = %s
            ORDER BY created_at DESC
            LIMIT 5
            """,
            (search_term, search_term),
        )

    rows = [_maintenance_request_public(row) for row in (cur.fetchall() or [])]
    return {
        "success": True,
        "message": "تم العثور على الطلبات" if rows else "لم يتم العثور على طلب مطابق",
        "data": {"items": rows},
    }


def _uberfix_get_request_details(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    row = _load_maintenance_request(cur, payload)
    _verify_request_phone(row, payload.get("client_phone"))
    return {
        "success": True,
        "message": "تم جلب تفاصيل الطلب",
        "data": _maintenance_request_public(row),
    }


def _uberfix_update_request(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    row = _load_maintenance_request(cur, payload)
    _verify_request_phone(row, payload.get("client_phone"), required=True)
    if row.get("workflow_stage") in {"closed", "paid", "cancelled"}:
        raise HTTPException(status_code=409, detail="لا يمكن تعديل طلب في مرحلة نهائية")

    updates = payload.get("updates") if isinstance(payload.get("updates"), dict) else {}
    allowed_columns = {
        "description": 1000,
        "location": 300,
        "priority": 20,
        "service_type": 60,
        "customer_notes": 1000,
        "title": 200,
        "latitude": None,
        "longitude": None,
        "workflow_stage": 40,
    }
    writable: dict[str, Any] = {}
    for column, max_len in allowed_columns.items():
        if column not in updates:
            continue
        value = updates[column]
        if column in {"latitude", "longitude"}:
            writable[column] = _numeric_or_none(value)
        elif column == "priority":
            value = _safe_gateway_text(value, max_len)
            if value in {"low", "medium", "normal", "high"}:
                writable[column] = value
        elif column == "workflow_stage":
            value = _safe_gateway_text(value, max_len)
            if value in {
                "submitted",
                "acknowledged",
                "on_hold",
                "cancelled",
                "scheduled",
            }:
                writable[column] = value
                writable["status"] = value
        else:
            writable[column] = _safe_gateway_text(value, max_len)

    if not writable:
        return {
            "success": True,
            "message": "لا توجد حقول قابلة للتعديل",
            "data": _maintenance_request_public(row),
        }

    columns = list(writable.keys())
    values = [writable[column] for column in columns]
    set_clause = ", ".join(f"{column} = %s" for column in columns)
    cur.execute(
        f"UPDATE maintenance_requests SET {set_clause} WHERE id = %s RETURNING *",
        (*values, row["id"]),
    )
    updated = cur.fetchone()
    _insert_uberfix_audit(
        cur,
        "BOT_UPDATE_REQUEST",
        "maintenance_request",
        updated["id"],
        row,
        updated,
        {"updated_fields": columns, "session_id": session_id},
    )
    return {
        "success": True,
        "message": "تم تحديث الطلب",
        "data": _maintenance_request_public(updated),
    }


def _uberfix_cancel_request(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    row = _load_maintenance_request(cur, payload)
    _verify_request_phone(row, payload.get("client_phone"), required=True)
    if row.get("workflow_stage") in {
        "in_progress",
        "completed",
        "billed",
        "paid",
        "closed",
    }:
        raise HTTPException(
            status_code=409,
            detail=f"لا يمكن إلغاء طلب في مرحلة {row.get('workflow_stage')}",
        )

    reason = _safe_gateway_text(
        payload.get("reason") or "إلغاء من العميل عبر البوت", 500
    )
    note = f"{datetime.now(timezone.utc).isoformat()} - إلغاء: {reason}"
    cur.execute(
        """
        UPDATE maintenance_requests
        SET workflow_stage = 'cancelled',
            status = 'cancelled',
            customer_notes = concat_ws(E'\n', nullif(customer_notes, ''), %s)
        WHERE id = %s
        RETURNING *
        """,
        (note, row["id"]),
    )
    updated = cur.fetchone()
    _insert_request_note(cur, row["id"], reason, "customer", "bot")
    _insert_uberfix_audit(
        cur,
        "BOT_CANCEL_REQUEST",
        "maintenance_request",
        updated["id"],
        row,
        updated,
        {"reason": reason, "session_id": session_id},
    )
    return {
        "success": True,
        "message": "تم إلغاء الطلب",
        "data": _maintenance_request_public(updated),
    }


def _uberfix_add_note(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    row = _load_maintenance_request(cur, payload)
    _verify_request_phone(row, payload.get("client_phone"), required=True)
    note = _require_payload_text(payload, "note", "نص الملاحظة مطلوب", 1000)
    stamped_note = f"{datetime.now(timezone.utc).isoformat()} - {note}"
    _insert_request_note(cur, row["id"], note, "customer", "bot")
    cur.execute(
        """
        UPDATE maintenance_requests
        SET customer_notes = concat_ws(E'\n', nullif(customer_notes, ''), %s)
        WHERE id = %s
        RETURNING *
        """,
        (stamped_note, row["id"]),
    )
    updated = cur.fetchone()
    return {
        "success": True,
        "message": "تمت إضافة الملاحظة",
        "data": _maintenance_request_public(updated),
    }


def _uberfix_assign_technician(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    row = _load_maintenance_request(cur, payload)
    technician_id = _safe_gateway_text(payload.get("technician_id"), 80)
    if payload.get("auto") and not technician_id:
        cur.execute(
            """
            SELECT *
            FROM maintenance_technicians
            WHERE is_active = true
              AND is_verified = true
              AND (specialization = %s OR %s = 'general')
            ORDER BY rating DESC NULLS LAST, review_count DESC
            LIMIT 1
            """,
            (row.get("service_type"), row.get("service_type")),
        )
        technician = cur.fetchone()
    else:
        cur.execute(
            """
            SELECT *
            FROM maintenance_technicians
            WHERE id::text = %s
              AND is_active = true
            LIMIT 1
            """,
            (technician_id,),
        )
        technician = cur.fetchone()

    if not technician:
        raise HTTPException(status_code=404, detail="لا يوجد فني مناسب حالياً")

    cur.execute(
        """
        UPDATE maintenance_requests
        SET assigned_technician_id = %s,
            technician_name = %s,
            workflow_stage = CASE WHEN workflow_stage = 'submitted' THEN 'acknowledged' ELSE workflow_stage END,
            status = CASE WHEN status = 'submitted' THEN 'acknowledged' ELSE status END
        WHERE id = %s
        RETURNING *
        """,
        (technician["id"], technician["name"], row["id"]),
    )
    updated = cur.fetchone()
    return {
        "success": True,
        "message": f"تم تعيين الفني {technician['name']}",
        "data": {
            "request": _maintenance_request_public(updated),
            "technician": _jsonable(technician),
        },
    }


def _uberfix_list_technicians(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    specialization = _safe_gateway_text(payload.get("specialization"), 80)
    limit = min(max(int(payload.get("limit") or 10), 1), 50)
    if specialization:
        cur.execute(
            """
            SELECT *
            FROM maintenance_technicians
            WHERE is_active = true AND is_verified = true AND specialization = %s
            ORDER BY rating DESC NULLS LAST, review_count DESC
            LIMIT %s
            """,
            (specialization, limit),
        )
    else:
        cur.execute(
            """
            SELECT *
            FROM maintenance_technicians
            WHERE is_active = true AND is_verified = true
            ORDER BY rating DESC NULLS LAST, review_count DESC
            LIMIT %s
            """,
            (limit,),
        )
    return {
        "success": True,
        "message": "تم جلب الفنيين",
        "data": {"items": cur.fetchall() or []},
    }


def _uberfix_list_categories(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    cur.execute(
        """
        SELECT key, label_ar AS label, label_en, sort_order
        FROM maintenance_categories
        WHERE is_active = true
        ORDER BY sort_order, label_ar
        """
    )
    rows = cur.fetchall() or []
    if not rows:
        rows = [dict(item) for item in UBERFIX_SERVICE_TYPES]
    return {"success": True, "message": "تم جلب فئات الصيانة", "data": {"items": rows}}


def _uberfix_list_services(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    return {
        "success": True,
        "message": "تم جلب أنواع الخدمات",
        "data": {"items": [dict(item) for item in UBERFIX_SERVICE_TYPES]},
    }


def _uberfix_get_branches(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    cur.execute(
        """
        SELECT *
        FROM branches
        WHERE is_active = true
        ORDER BY name
        LIMIT 100
        """
    )
    return {
        "success": True,
        "message": "تم جلب الفروع",
        "data": {"items": cur.fetchall() or []},
    }


def _uberfix_find_nearest_branch(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    latitude = _numeric_or_none(payload.get("latitude"))
    longitude = _numeric_or_none(payload.get("longitude"))
    if latitude is None or longitude is None:
        raise HTTPException(status_code=400, detail="latitude و longitude مطلوبان")
    city = _safe_gateway_text(payload.get("city"), 120)
    params: list[Any] = [latitude, longitude, latitude]
    city_filter = ""
    if city:
        city_filter = "AND city ILIKE %s"
        params.append(f"%{city}%")
    cur.execute(
        f"""
        SELECT *,
               sqrt(
                 power((latitude - %s) * 111.0, 2) +
                 power((longitude - %s) * 111.0 * cos(radians(%s)), 2)
               ) AS distance_km
        FROM branches
        WHERE is_active = true
          AND latitude IS NOT NULL
          AND longitude IS NOT NULL
          {city_filter}
        ORDER BY distance_km
        LIMIT 5
        """,
        tuple(params),
    )
    return {
        "success": True,
        "message": "تم جلب أقرب الفروع",
        "data": {"items": cur.fetchall() or []},
    }


def _uberfix_collect_customer_info(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id مطلوب لحفظ سياق العميل")
    client_phone = _require_payload_text(
        payload, "client_phone", "رقم هاتف العميل مطلوب", 40
    )
    context = {
        "notes": _safe_gateway_text(payload.get("notes"), 1000),
        "metadata": metadata,
    }
    from psycopg.types.json import Jsonb

    cur.execute(
        """
        INSERT INTO bot_sessions (
            session_id, client_phone, client_name, client_email, location,
            latitude, longitude, preferred_branch_id, context
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, NULLIF(%s, '')::uuid, %s)
        ON CONFLICT (session_id) DO UPDATE SET
            client_phone = EXCLUDED.client_phone,
            client_name = coalesce(EXCLUDED.client_name, bot_sessions.client_name),
            client_email = coalesce(EXCLUDED.client_email, bot_sessions.client_email),
            location = coalesce(EXCLUDED.location, bot_sessions.location),
            latitude = coalesce(EXCLUDED.latitude, bot_sessions.latitude),
            longitude = coalesce(EXCLUDED.longitude, bot_sessions.longitude),
            preferred_branch_id = coalesce(EXCLUDED.preferred_branch_id, bot_sessions.preferred_branch_id),
            context = bot_sessions.context || EXCLUDED.context,
            expires_at = now() + interval '7 days'
        RETURNING *
        """,
        (
            session_id,
            client_phone,
            _safe_gateway_text(payload.get("client_name"), 120) or None,
            _safe_gateway_text(payload.get("client_email"), 180) or None,
            _safe_gateway_text(payload.get("location"), 300) or None,
            _numeric_or_none(payload.get("latitude")),
            _numeric_or_none(payload.get("longitude")),
            _safe_gateway_text(payload.get("preferred_branch_id"), 80),
            Jsonb(context),
        ),
    )
    session_row = cur.fetchone()
    previous = _find_latest_request_by_phone(cur, client_phone)
    return {
        "success": True,
        "message": "تم حفظ بيانات العميل في السياق",
        "data": {
            "is_returning_customer": bool(previous),
            "previous_data": _maintenance_request_public(previous)
            if previous
            else None,
            "collected": _jsonable(session_row),
        },
    }


def _uberfix_get_quote(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    service_type = _safe_gateway_text(payload.get("service_type") or "general", 80)
    description = _safe_gateway_text(payload.get("description"), 1000)
    return {
        "success": True,
        "message": "تم استلام بيانات عرض السعر. يحتاج الفريق لمراجعة التفاصيل قبل تسعير نهائي.",
        "data": {
            "service_type": service_type,
            "description": description,
            "requires_human_review": True,
        },
    }


def _load_maintenance_request(cur, payload: dict[str, Any]) -> dict[str, Any]:
    request_id = _safe_gateway_text(payload.get("request_id"), 80)
    request_number = _safe_gateway_text(
        payload.get("request_number") or payload.get("tracking_number"), 80
    )
    if not request_id and not request_number:
        raise HTTPException(
            status_code=400, detail="request_id أو request_number مطلوب"
        )
    if request_id:
        cur.execute(
            "SELECT * FROM maintenance_requests WHERE id::text = %s LIMIT 1",
            (request_id,),
        )
    else:
        cur.execute(
            "SELECT * FROM maintenance_requests WHERE upper(request_number) = upper(%s) LIMIT 1",
            (request_number,),
        )
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    return row


def _uberfix_get_status(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    row = _load_maintenance_request(cur, payload)
    return {
        "success": True,
        "request_id": str(row["id"]),
        "request_number": row.get("request_number"),
        "status": row.get("status"),
        "workflow_stage": row.get("workflow_stage"),
        "workflow_stage_v2": row.get("workflow_stage"),
        "track_url": row.get("track_url"),
        "created_at": _jsonable(row.get("created_at")),
        "updated_at": _jsonable(row.get("updated_at")),
    }


def _uberfix_transition_stage(
    cur,
    payload: dict[str, Any],
    session_id: Optional[str],
    metadata: dict[str, Any],
) -> dict[str, Any]:
    row = _load_maintenance_request(cur, payload)
    to_stage = _require_payload_text(payload, "to_stage", "to_stage مطلوب", 40)
    reason = _safe_gateway_text(payload.get("reason"), 500) or "تغيير المرحلة عبر البوت"
    from_stage = row.get("workflow_stage")

    cur.execute(
        """
        UPDATE maintenance_requests
        SET workflow_stage = %s,
            status = %s,
            updated_at = now()
        WHERE id = %s
        RETURNING *
        """,
        (to_stage, to_stage, row["id"]),
    )
    updated = cur.fetchone()

    _insert_request_note(
        cur,
        row["id"],
        f"تغيير المرحلة من {from_stage} إلى {to_stage}: {reason}",
        "system",
        "bot",
    )
    _insert_uberfix_audit(
        cur,
        "BOT_TRANSITION_STAGE",
        "maintenance_request",
        updated["id"],
        row,
        updated,
        {
            "from_stage": from_stage,
            "to_stage": to_stage,
            "reason": reason,
            "session_id": session_id,
        },
    )

    return {
        "success": True,
        "request_id": str(updated["id"]),
        "request_number": updated.get("request_number"),
        "from_stage": from_stage,
        "to_stage": to_stage,
        "track_url": updated.get("track_url"),
    }


def _find_latest_request_by_phone(cur, phone: str) -> Optional[dict[str, Any]]:
    tail = _phone_digits(phone)[-9:]
    if not tail:
        return None
    cur.execute(
        """
        SELECT *
        FROM maintenance_requests
        WHERE regexp_replace(coalesce(client_phone, ''), '\\D', '', 'g') LIKE %s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (f"%{tail}",),
    )
    return cur.fetchone()


def _verify_request_phone(
    row: dict[str, Any], provided_phone: Any, *, required: bool = False
) -> None:
    if not provided_phone and not required:
        return
    if not provided_phone:
        raise HTTPException(status_code=400, detail="client_phone مطلوب للتحقق")
    stored_tail = _phone_digits(row.get("client_phone"))[-9:]
    provided_tail = _phone_digits(provided_phone)[-9:]
    if not stored_tail or stored_tail != provided_tail:
        raise HTTPException(status_code=403, detail="غير مصرح بالوصول لهذا الطلب")


def _insert_request_note(
    cur, request_id: Any, note: str, note_type: str, created_by: str
) -> None:
    cur.execute(
        """
        INSERT INTO maintenance_request_notes (request_id, note, note_type, created_by)
        VALUES (%s, %s, %s, %s)
        """,
        (request_id, note, note_type, created_by),
    )


def _insert_uberfix_audit(
    cur,
    action: str,
    entity_type: str,
    entity_id: Any,
    old_values: Optional[dict[str, Any]],
    new_values: Optional[dict[str, Any]],
    metadata: dict[str, Any],
) -> None:
    from psycopg.types.json import Jsonb

    cur.execute(
        """
        INSERT INTO audit_logs (
            actor_type, actor_id, action, entity_type, entity_id,
            old_values, new_values, metadata
        )
        VALUES ('bot', 'azabot', %s, %s, %s, %s, %s, %s)
        """,
        (
            action,
            entity_type,
            entity_id,
            Jsonb(_jsonable(old_values)) if old_values else None,
            Jsonb(_jsonable(new_values)) if new_values else None,
            Jsonb(_jsonable(metadata)),
        ),
    )


def _insert_uberfix_gateway_log(
    cur,
    consumer: Optional[dict[str, Any]],
    request_context: dict[str, Any],
    action: str,
    request_payload: dict[str, Any],
    response_payload: dict[str, Any],
    status_code: int,
    duration_seconds: float,
    error_message: str,
) -> None:
    from psycopg.types.json import Jsonb

    cur.execute(
        """
        INSERT INTO api_gateway_logs (
            consumer_id, route, action, request_payload, response_payload,
            status_code, success, duration_ms, ip_address, user_agent, error_message
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULLIF(%s, '')::inet, %s, %s)
        """,
        (
            consumer.get("id") if consumer else None,
            request_context.get("route") or "/uberfix/bot-gateway",
            action,
            Jsonb(_jsonable(_scrub_gateway_request_for_log(request_payload))),
            Jsonb(_jsonable(response_payload)),
            status_code,
            bool(response_payload.get("success")),
            int(duration_seconds * 1000),
            request_context.get("client_ip") or "",
            request_context.get("user_agent"),
            error_message,
        ),
    )


def _log_uberfix_gateway_failure(
    conn,
    consumer: Optional[dict[str, Any]],
    request_context: dict[str, Any],
    action: str,
    request_payload: dict[str, Any],
    response_payload: dict[str, Any],
    status_code: int,
    duration_seconds: float,
    error_message: str,
) -> None:
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            _insert_uberfix_gateway_log(
                cur,
                consumer,
                request_context,
                action,
                request_payload,
                response_payload,
                status_code,
                duration_seconds,
                error_message,
            )
        conn.commit()
    except Exception as exc:
        conn.rollback()
        logger.warning("Failed to write UberFix gateway error log: %s", exc)


def _scrub_gateway_request_for_log(payload: dict[str, Any]) -> dict[str, Any]:
    scrubbed = dict(payload)
    if "api_key" in scrubbed:
        scrubbed["api_key"] = "***"
    return scrubbed


def _maintenance_request_public(row: dict[str, Any]) -> dict[str, Any]:
    return _jsonable(
        {
            "request_id": row.get("id"),
            "id": row.get("id"),
            "request_number": row.get("request_number"),
            "tracking_number": row.get("request_number"),
            "client_name": row.get("client_name"),
            "client_phone": row.get("client_phone"),
            "location": row.get("location"),
            "service_type": row.get("service_type"),
            "title": row.get("title"),
            "description": row.get("description"),
            "priority": row.get("priority"),
            "status": row.get("status"),
            "workflow_stage": row.get("workflow_stage"),
            "technician_name": row.get("technician_name"),
            "eta": row.get("eta"),
            "scheduled_at": row.get("scheduled_at"),
            "track_url": row.get("track_url")
            or f"{UBERFIX_TRACK_BASE_URL}/{row.get('request_number') or row.get('id')}",
            "created_at": row.get("created_at"),
            "updated_at": row.get("updated_at"),
        }
    )


def _safe_gateway_text(value: Any, max_len: int) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return text[:max_len]


def _require_payload_text(
    payload: dict[str, Any], key: str, error: str, max_len: int
) -> str:
    value = _safe_gateway_text(payload.get(key), max_len)
    if not value:
        raise HTTPException(status_code=400, detail=error)
    return value


def _numeric_or_none(value: Any) -> Optional[float]:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _is_relative_to(child: Path, parent: Path) -> bool:
    """التحقق من أن المسار يقع داخل المجلد المسموح به (حماية من Path Traversal)."""
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except (ValueError, RuntimeError):
        return False


def _phone_digits(value: Any) -> str:
    return re.sub(r"\D+", "", str(value or ""))


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, uuid.UUID):
        return str(value)
    return value


# ══════════════════════════════════════════════════════════════
#  SYSTEM ENDPOINTS


# ══════════════════════════════════════════════════════════════
#  Public Entry Point
# ══════════════════════════════════════════════════════════════

def _handle_uberfix_gateway_sync(
    body: dict[str, Any],
    request_context: dict[str, Any],
) -> tuple[dict[str, Any], int]:
    """المُنسّق الرئيسي — يربط auth + rate limit + action + logging."""
    import time as _time
    started = _time.time()
    conn = None
    consumer: dict[str, Any] | None = None
    action = str(body.get("action") or "").strip()
    response_payload: dict[str, Any]
    status_code = 200
    error_message = ""

    try:
        conn = _uberfix_db_connect()
        with conn.cursor() as cur:
            consumer = _authenticate_uberfix_gateway(cur, request_context)
            _enforce_uberfix_rate_limit(cur, consumer)
            response_payload = _execute_uberfix_action(
                cur,
                action,
                body.get("payload") if isinstance(body.get("payload"), dict) else {},
                str(body.get("session_id") or "").strip() or None,
                body.get("metadata") if isinstance(body.get("metadata"), dict) else {},
            )
            status_code = 200 if response_payload.get("success") else 400
            _insert_uberfix_gateway_log(
                cur, consumer, request_context, action, body,
                response_payload, status_code, _time.time() - started, error_message,
            )
        conn.commit()

    except HTTPException as exc:
        if conn:
            conn.rollback()
        status_code = exc.status_code
        error_message = str(exc.detail)
        response_payload = {"success": False, "error": error_message}
        _log_uberfix_gateway_failure(
            conn, consumer, request_context, action, body,
            response_payload, status_code, _time.time() - started, error_message,
        )

    except Exception as exc:
        if conn:
            conn.rollback()
        status_code = 500
        error_message = "حدث خطأ داخلي في بوابة UberFix"
        logger.exception("UberFix bot-gateway failed: %s", exc)
        response_payload = {"success": False, "error": error_message}
        _log_uberfix_gateway_failure(
            conn, consumer, request_context, action, body,
            response_payload, status_code, _time.time() - started, str(exc),
        )

    finally:
        if conn:
            conn.close()

    return _jsonable(response_payload), status_code


def handle_uberfix_gateway_sync(
    body: dict[str, Any],
    request_context: dict[str, Any],
) -> tuple[dict[str, Any], int]:
    """
    نقطة الدخول الرئيسية — تُستدعى من server.py عبر run_in_threadpool.
    (sync لأن psycopg sync client)
    """
    return _handle_uberfix_gateway_sync(body, request_context)
