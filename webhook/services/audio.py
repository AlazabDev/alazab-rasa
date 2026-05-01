"""
webhook/services/audio.py — Audio Transcription & TTS
======================================================
"""

from __future__ import annotations

import logging
import os
import re
from typing import Optional

from fastapi import HTTPException
from openai import AsyncOpenAI

from ..config import (
    AUDIO_TRANSCRIPTION_MODEL,
    AUDIO_TTS_MODEL,
    AUDIO_TTS_VOICE,
    PIPER_PRONUNCIATION_LEXICON_FILE,
)

logger = logging.getLogger("alazab.webhook.audio")


async def transcribe_audio(audio_path: str) -> Optional[str]:
    """Transcribe audio file to text using OpenAI."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    organization = os.getenv("OPENAI_ORG_ID", "").strip() or None
    project = os.getenv("OPENAI_PROJECT_ID", "").strip() or None
    if not api_key or api_key.startswith("replace-with-"):
        return None

    try:
        client = AsyncOpenAI(api_key=api_key, organization=organization, project=project)
        with open(audio_path, "rb") as audio_file:
            transcript = await client.audio.transcriptions.create(
                model=AUDIO_TRANSCRIPTION_MODEL,
                file=audio_file,
            )
        text = getattr(transcript, "text", None)
        if isinstance(text, str):
            text = text.strip()
            return text or None

        if isinstance(transcript, dict):
            dict_text = str(transcript.get("text", "")).strip()
            return dict_text or None

        return None
    except Exception as exc:
        logger.error("Audio transcription failed: %s", exc)
        return None


async def text_to_speech(text: str, voice: Optional[str], model: Optional[str]) -> bytes:
    """Convert text to speech using OpenAI TTS."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    organization = os.getenv("OPENAI_ORG_ID", "").strip() or None
    project = os.getenv("OPENAI_PROJECT_ID", "").strip() or None
    if not api_key or api_key.startswith("replace-with-"):
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")

    selected_voice = (voice or AUDIO_TTS_VOICE).strip() or AUDIO_TTS_VOICE
    selected_model = (model or AUDIO_TTS_MODEL).strip() or AUDIO_TTS_MODEL

    try:
        client = AsyncOpenAI(api_key=api_key, organization=organization, project=project)
        speech = await client.audio.speech.create(
            model=selected_model,
            voice=selected_voice,
            input=_apply_tts_pronunciation_lexicon(text).strip()[:4000],
            response_format="mp3",
        )
        if hasattr(speech, "aread"):
            return await speech.aread()
        if hasattr(speech, "content"):
            return speech.content
        return speech.read()
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Text-to-speech failed: %s", exc)
        raise HTTPException(status_code=502, detail="فشل تحويل النص إلى صوت")


# ── TTS Pronunciation Lexicon ────────────────────────────────
def _apply_tts_pronunciation_lexicon(text: str) -> str:
    output = text
    for source, target in _load_tts_pronunciation_rules():
        if not source or not target:
            continue
        output = re.sub(re.escape(source), target, output)
    return output


def _load_tts_pronunciation_rules() -> list[tuple[str, str]]:
    if not PIPER_PRONUNCIATION_LEXICON_FILE.exists():
        return []

    try:
        lines = PIPER_PRONUNCIATION_LEXICON_FILE.read_text(encoding="utf-8").splitlines()
    except Exception:
        logger.exception("Failed to read TTS pronunciation lexicon")
        return []

    rules: list[tuple[str, str]] = []
    current_matches: list[str] = []
    current_written: Optional[str] = None
    in_match_block = False

    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- id:"):
            current_matches = []
            current_written = None
            in_match_block = False
            continue

        if stripped.startswith("- written:"):
            current_written = _yaml_scalar(stripped.split(":", 1)[1].strip())
            in_match_block = False
            continue

        if stripped.startswith("preferred_spoken:") and current_written:
            rules.append((current_written, _yaml_scalar(stripped.split(":", 1)[1].strip())))
            current_written = None
            continue

        if stripped == "match:":
            in_match_block = True
            continue

        if stripped.startswith("say_as:"):
            target = _yaml_scalar(stripped.split(":", 1)[1].strip())
            rules.extend((source, target) for source in current_matches)
            current_matches = []
            in_match_block = False
            continue

        if in_match_block and stripped.startswith("- "):
            current_matches.append(_yaml_scalar(stripped[2:].strip()))

    return sorted(rules, key=lambda item: len(item[0]), reverse=True)


def _yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value
