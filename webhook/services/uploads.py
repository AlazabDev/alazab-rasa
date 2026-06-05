"""
webhook/services/uploads.py — File Upload Handling
====================================================
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import HTTPException, UploadFile

from ..config import (
    MAX_UPLOAD_BYTES,
    PUBLIC_BASE_URL,
    UPLOADS_DIR,
    UPLOADS_PUBLIC_ENABLED,
)
from ..utils import sanitize_filename


import filetype
import mimetypes

async def save_upload(
    upload: UploadFile,
    allowed_extensions: set[str],
    *,
    kind: str,
) -> dict[str, Any]:
    """Save uploaded file and return metadata dict."""
    original_name = upload.filename or f"{kind}.bin"
    safe_name = sanitize_filename(original_name)
    extension = Path(safe_name).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(status_code=415, detail="نوع الملف غير مدعوم")

    content = await upload.read()
    if not content:
        raise HTTPException(status_code=400, detail="الملف فارغ")
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="حجم الملف أكبر من المسموح")

    # فحص نوع الملف عبر filetype أو mimetypes
    kind_obj = filetype.guess(content)
    if kind_obj is not None:
        mime = kind_obj.mime
    else:
        mime, _ = mimetypes.guess_type(safe_name)
        if not mime:
            mime = "application/octet-stream"
            
    allowed_mimes = {
        "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-powerpoint", "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "image/jpeg", "image/png", "image/webp", "image/gif", "text/plain", "text/csv", "application/zip",
        "audio/mpeg", "audio/wav", "audio/x-wav", "audio/ogg", "audio/mp4", "audio/aac", "audio/x-m4a", 
        "video/mp4", "video/webm", "application/octet-stream"
    }
    if mime not in allowed_mimes and not mime.startswith("text/"):
        raise HTTPException(status_code=415, detail=f"نوع الملف غير مدعوم أو مزيف ({mime})")

    bucket = datetime.now(timezone.utc).strftime("%Y/%m")
    target_dir = UPLOADS_DIR / bucket
    target_dir.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    target_name = f"{stamp}_{uuid.uuid4().hex[:10]}_{safe_name}"
    target_path = target_dir / target_name
    target_path.write_bytes(content)

    relative_url = f"/uploads/{bucket}/{target_name}"
    return {
        "id": str(uuid.uuid4()),
        "kind": kind,
        "name": safe_name,
        "size": len(content),
        "content_type": upload.content_type or "application/octet-stream",
        "relative_path": f"{bucket}/{target_name}",
        "url": f"{PUBLIC_BASE_URL}{relative_url}" if UPLOADS_PUBLIC_ENABLED else "",
        "path": str(target_path),
    }
