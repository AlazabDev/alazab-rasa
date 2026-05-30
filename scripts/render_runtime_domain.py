#!/usr/bin/env python3
"""
Generate runtime-ready Rasa files from tracked templates.

Outputs:
- .runtime/domain.generated.yml
- .runtime/endpoints.generated.yml

Production rule:
- domain.yml is the root domain source and may include additional domain files.
- endpoints.yml is the only tracked endpoint template.
- Environment placeholders are rendered before Rasa starts.
- Missing required values fail closed.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / ".runtime"
DOMAIN_SOURCE = ROOT / "domain.yml"
DOMAIN_OUTPUT = RUNTIME_DIR / "domain.generated.yml"
ENDPOINTS_SOURCE = ROOT / "endpoints.yml"
ENDPOINTS_OUTPUT = RUNTIME_DIR / "endpoints.generated.yml"

LIST_KEYS = {"intents", "entities", "actions", "e2e_actions", "forms"}
DICT_KEYS = {"slots", "responses", "session_config"}
ENV_PATTERN = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-(.*?))?\}")

REQUIRED_MODEL_GROUPS = {
    "command_generator_llm",
    "enterprise_search_generation",
    "enterprise_search_embeddings",
    "openai-gpt-4o",
    "openai-gpt-4o-mini",
}


class RuntimeRenderError(RuntimeError):
    """Raised when tracked templates cannot produce safe runtime files."""


def _atomic_write(path: Path, content: str) -> None:
    """Write a runtime file atomically to avoid partial files during restart."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise RuntimeRenderError(f"Missing required file: {path.relative_to(ROOT)}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise RuntimeRenderError(f"Invalid YAML: {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeRenderError(f"Expected YAML mapping: {path.relative_to(ROOT)}")
    return data


def _safe_include_path(relative_path: str) -> Path:
    candidate = (ROOT / relative_path).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise RuntimeRenderError(f"Domain include escapes repository root: {relative_path}") from exc
    return candidate


def _merge_unique_list(destination: list[Any], source: list[Any]) -> list[Any]:
    seen = {
        yaml.safe_dump(item, allow_unicode=True, sort_keys=True)
        for item in destination
    }
    for item in source:
        key = yaml.safe_dump(item, allow_unicode=True, sort_keys=True)
        if key not in seen:
            destination.append(item)
            seen.add(key)
    return destination


def _render_domain() -> None:
    root_domain = _load_yaml_mapping(DOMAIN_SOURCE)
    includes = root_domain.pop("includes", []) or []
    if not isinstance(includes, list):
        raise RuntimeRenderError("domain.yml includes must be a list")

    merged: dict[str, Any] = dict(root_domain)

    for relative_path in includes:
        if not isinstance(relative_path, str) or not relative_path.strip():
            raise RuntimeRenderError("domain.yml contains an invalid include entry")
        include_path = _safe_include_path(relative_path.strip())
        included = _load_yaml_mapping(include_path)

        for key, value in included.items():
            if key == "version":
                merged.setdefault("version", value)
            elif key in LIST_KEYS and isinstance(value, list):
                merged[key] = _merge_unique_list(merged.get(key, []), value)
            elif key in DICT_KEYS and isinstance(value, dict):
                current = merged.setdefault(key, {})
                if not isinstance(current, dict):
                    raise RuntimeRenderError(f"Domain key must be a mapping: {key}")
                for child_key, child_value in value.items():
                    if child_key in current and current[child_key] != child_value:
                        print(
                            f"[render-runtime][WARN] overriding duplicate domain key "
                            f"{key}.{child_key} from {relative_path}",
                            file=sys.stderr,
                        )
                    current[child_key] = child_value
            elif key not in merged:
                merged[key] = value

    if not merged.get("version"):
        raise RuntimeRenderError("Generated domain is missing version")

    _atomic_write(
        DOMAIN_OUTPUT,
        yaml.safe_dump(merged, allow_unicode=True, sort_keys=False, width=1000),
    )


def _render_environment_placeholders(text: str) -> str:
    missing: set[str] = set()

    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        default = match.group(2)
        value = os.getenv(name)
        if value is None or value == "":
            if default is not None:
                return default
            missing.add(name)
            return match.group(0)
        return value

    rendered = ENV_PATTERN.sub(replace, text)
    if missing:
        names = ", ".join(sorted(missing))
        raise RuntimeRenderError(f"Missing required environment variables: {names}")
    if ENV_PATTERN.search(rendered):
        raise RuntimeRenderError("Unresolved environment placeholders remain in endpoints.yml")
    return rendered


def _validate_endpoints(data: dict[str, Any]) -> None:
    action_endpoint = data.get("action_endpoint") or {}
    action_url = str(action_endpoint.get("url") or "").strip()
    if not action_url.startswith(("http://", "https://")):
        raise RuntimeRenderError("action_endpoint.url must be an HTTP URL")

    tracker_store = data.get("tracker_store") or {}
    tracker_url = str(tracker_store.get("url") or "").strip()
    if tracker_store.get("type") != "SQL":
        raise RuntimeRenderError("tracker_store.type must be SQL")
    if str(tracker_store.get("dialect") or "").lower() != "postgresql":
        raise RuntimeRenderError("tracker_store.dialect must be postgresql")
    if not tracker_url.startswith(("postgresql://", "postgres://")):
        raise RuntimeRenderError("DATABASE_URL must be a PostgreSQL connection URL")

    lock_store = data.get("lock_store") or {}
    if lock_store.get("type") != "redis":
        raise RuntimeRenderError("lock_store.type must be redis")
    if not str(lock_store.get("url") or "").strip():
        raise RuntimeRenderError("Redis host is required")
    try:
        redis_port = int(lock_store.get("port"))
        redis_db = int(lock_store.get("db"))
    except (TypeError, ValueError) as exc:
        raise RuntimeRenderError("Redis port and db must be integers") from exc
    if not 1 <= redis_port <= 65535:
        raise RuntimeRenderError("Redis port is outside the valid range")
    if redis_db < 0:
        raise RuntimeRenderError("Redis db must be zero or greater")

    groups = data.get("model_groups")
    if not isinstance(groups, list):
        raise RuntimeRenderError("model_groups must be a list")
    ids = {str(item.get("id")) for item in groups if isinstance(item, dict)}
    missing_groups = REQUIRED_MODEL_GROUPS - ids
    if missing_groups:
        names = ", ".join(sorted(missing_groups))
        raise RuntimeRenderError(f"Missing required model groups: {names}")


def _render_endpoints() -> None:
    if not ENDPOINTS_SOURCE.exists():
        raise RuntimeRenderError("Missing required file: endpoints.yml")

    template = ENDPOINTS_SOURCE.read_text(encoding="utf-8")
    rendered = _render_environment_placeholders(template)

    try:
        endpoints = yaml.safe_load(rendered) or {}
    except yaml.YAMLError as exc:
        raise RuntimeRenderError(f"Rendered endpoints YAML is invalid: {exc}") from exc

    if not isinstance(endpoints, dict):
        raise RuntimeRenderError("Rendered endpoints must be a YAML mapping")

    _validate_endpoints(endpoints)
    _atomic_write(
        ENDPOINTS_OUTPUT,
        yaml.safe_dump(endpoints, allow_unicode=True, sort_keys=False, width=1000),
    )


def main() -> int:
    try:
        _render_domain()
        _render_endpoints()
    except RuntimeRenderError as exc:
        print(f"[render-runtime][FAIL] {exc}", file=sys.stderr)
        return 1

    print(f"[render-runtime][OK] {DOMAIN_OUTPUT.relative_to(ROOT)}")
    print(f"[render-runtime][OK] {ENDPOINTS_OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
