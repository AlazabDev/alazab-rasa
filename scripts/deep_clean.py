#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
COL = {
    "red": "\033[1;31m", "yellow": "\033[1;33m", "green": "\033[1;32m",
    "blue": "\033[1;34m", "purple": "\033[1;35m", "nc": "\033[0m",
}

def say(kind: str, msg: str) -> None:
    icons = {"err":"🔴", "warn":"🟡", "ok":"🟢", "info":"🔵", "work":"🟣"}
    colors = {"err":"red", "warn":"yellow", "ok":"green", "info":"blue", "work":"purple"}
    print(f"{COL[colors[kind]]}{icons[kind]} {msg}{COL['nc']}")

def run(cmd: list[str], check: bool = True) -> int:
    say("work", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=ROOT)
    if check and proc.returncode:
        raise SystemExit(proc.returncode)
    return proc.returncode

def yaml_files() -> list[Path]:
    return [ROOT / "domain.yml", ROOT / "config.yml", ROOT / "endpoints.yml", ROOT / "endpoints.sqlite.yml"] + sorted((ROOT / "domain").glob("*.yml")) + sorted((ROOT / "data").rglob("*.yml"))

def validate_yaml() -> None:
    seen: dict[str, list[str]] = {}
    for path in yaml_files():
        if not path.exists():
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception as exc:
            say("err", f"YAML invalid: {path.relative_to(ROOT)}: {exc}")
            raise SystemExit(1)
        responses = data.get("responses")
        if path.parts[-2:-1] == ("data",) and responses:
            say("warn", f"responses found in data file: {path.relative_to(ROOT)}")
        if isinstance(responses, dict):
            for key in responses:
                seen.setdefault(key, []).append(str(path.relative_to(ROOT)))
    dups = {k:v for k,v in seen.items() if len(v) > 1}
    if dups:
        for key, paths in dups.items():
            say("err", f"duplicate response {key}: {', '.join(paths)}")
        raise SystemExit(1)
    say("ok", "YAML validation and response duplicate check passed")

def backup_models() -> None:
    models = ROOT / "models"
    if models.exists() and any(models.iterdir()):
        stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        target = ROOT / "_repair_reports" / f"models_restore_{stamp}"
        target.parent.mkdir(exist_ok=True)
        shutil.copytree(models, target)
        say("info", f"models restore point: {target.relative_to(ROOT)}")

def clean_models_and_cache() -> None:
    backup_models()
    for rel in ["models", ".rasa", ".runtime/faiss", ".cache/rasa"]:
        path = ROOT / rel
        if path.exists():
            shutil.rmtree(path)
            say("ok", f"removed {rel}")
    (ROOT / "models").mkdir(exist_ok=True)
    (ROOT / ".runtime").mkdir(exist_ok=True)

def rebuild_sqlite_if_needed() -> None:
    db = ROOT / ".runtime" / "tracker.db"
    if not db.exists():
        say("info", "SQLite tracker db does not exist; Rasa will create it on start")
        return
    try:
        con = sqlite3.connect(db)
        con.execute("pragma integrity_check")
        con.close()
        say("ok", "SQLite tracker db integrity check passed")
    except sqlite3.DatabaseError:
        broken = db.with_suffix(".broken")
        shutil.move(db, broken)
        say("warn", f"moved broken SQLite db to {broken.relative_to(ROOT)}")

def fix_duplicate_intents() -> None:
    domain = ROOT / "domain.yml"
    data = yaml.safe_load(domain.read_text(encoding="utf-8")) or {}
    intents = data.get("intents")
    if isinstance(intents, list):
        cleaned = []
        seen = set()
        for item in intents:
            key = item if isinstance(item, str) else next(iter(item.keys()), str(item)) if isinstance(item, dict) else str(item)
            if key not in seen:
                cleaned.append(item)
                seen.add(key)
        if len(cleaned) != len(intents):
            data["intents"] = cleaned
            domain.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
            say("ok", f"removed {len(intents)-len(cleaned)} duplicate domain intent mappings")
        else:
            say("ok", "no duplicate domain intent mappings found")

def _split_examples(text: str) -> list[str]:
    examples: list[str] = []
    for line in (text or "").splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            examples.append(stripped[2:].strip())
    return examples


def _build_examples(examples: list[str]) -> str:
    return "".join(f"- {example}\n" for example in examples)


def fix_duplicate_nlu_examples() -> None:
    seen: dict[str, tuple[str, str]] = {}
    removed = 0
    for path in sorted((ROOT / "data").rglob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        changed = False
        for item in data.get("nlu") or []:
            intent = item.get("intent")
            if not intent or "examples" not in item:
                continue
            kept: list[str] = []
            for example in _split_examples(item.get("examples") or ""):
                norm = " ".join(example.split())
                if norm in seen and seen[norm][1] != intent:
                    removed += 1
                    changed = True
                    continue
                seen.setdefault(norm, (str(path.relative_to(ROOT)), intent))
                kept.append(example)
            item["examples"] = _build_examples(kept)
        if changed:
            path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
    if removed:
        say("ok", f"removed {removed} duplicate NLU examples across different intents")
    else:
        say("ok", "no duplicate NLU examples across different intents found")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--skip-train", action="store_true")
    args = parser.parse_args()

    validate_yaml()
    fix_duplicate_intents()
    fix_duplicate_nlu_examples()
    validate_yaml()
    if args.validate_only:
        return 0
    clean_models_and_cache()
    rebuild_sqlite_if_needed()
    if not args.skip_train:
        run(["bash", "scripts/botctl.sh", "train"], check=True)
    say("ok", "deep clean completed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
