#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".runtime" / "domain.generated.yml"
LIST_KEYS = {"intents", "entities", "actions", "e2e_actions", "forms"}
DICT_KEYS = {"slots", "responses", "session_config"}


def merge_unique_list(dst: list, src: list) -> list:
    seen = {yaml.safe_dump(item, allow_unicode=True, sort_keys=True) for item in dst}
    for item in src:
        key = yaml.safe_dump(item, allow_unicode=True, sort_keys=True)
        if key not in seen:
            dst.append(item)
            seen.add(key)
    return dst


def main() -> int:
    root_path = ROOT / "domain.yml"
    root = yaml.safe_load(root_path.read_text(encoding="utf-8")) or {}
    includes = root.pop("includes", []) or []
    merged = dict(root)
    # Keep responses from domain.yml
    # merged.pop("responses", None)
    for rel in includes:
        path = ROOT / rel
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for key, value in data.items():
            if key == "version":
                merged.setdefault("version", value)
            elif key in LIST_KEYS and isinstance(value, list):
                merged[key] = merge_unique_list(merged.get(key, []), value)
            elif key in DICT_KEYS and isinstance(value, dict):
                current = merged.setdefault(key, {})
                for child_key, child_value in value.items():
                    if child_key in current and current[child_key] != child_value:
                        print(
                            f"Warning: Overwriting duplicate domain key {key}.{child_key} from {rel}",
                            file=sys.stderr,
                        )
                    current[child_key] = child_value
            elif key not in merged:
                merged[key] = value

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(
        yaml.safe_dump(merged, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# ── توليد endpoints.generated.yml ────────────────────────────
import shutil
ENDPOINTS_OUT = ROOT / ".runtime" / "endpoints.generated.yml"
ENDPOINTS_SRC = ROOT / "endpoints.nodocker.yml"
if ENDPOINTS_SRC.exists():
    shutil.copy(ENDPOINTS_SRC, ENDPOINTS_OUT)
