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
