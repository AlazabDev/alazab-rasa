#!/usr/bin/env python3
"""AzaBot Rasa training-data audit.

Checks the files that feed Rasa training before running expensive training:
- domain include integrity
- generated domain integrity
- actions/responses/slots/intents referenced by flows/rules/stories
- accidental domain sections inside data/*.yml files
- custom actions declared in domain but not implemented locally
- duplicate NLU blocks and weak NLU coverage warnings
"""
from __future__ import annotations

import argparse
import ast
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
DOMAIN_SOURCE = ROOT / "domain.yml"
DOMAIN_GENERATED = ROOT / ".runtime" / "domain.generated.yml"
DATA_DIR = ROOT / "data"

DOMAIN_ONLY_KEYS = {"responses", "actions", "slots", "forms", "entities", "session_config"}
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "models", ".runtime", "__pycache__"}


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        raise RuntimeError(f"YAML read failed: {path.relative_to(ROOT)}: {exc}") from exc


def iter_yaml_files(base: Path):
    for path in sorted(base.rglob("*.yml")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path
    for path in sorted(base.rglob("*.yaml")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def as_intent_set(intents: list[Any]) -> set[str]:
    result: set[str] = set()
    for item in intents or []:
        if isinstance(item, str):
            result.add(item)
        elif isinstance(item, dict):
            result.update(str(k) for k in item.keys())
    return result


def render_runtime() -> None:
    subprocess.run(
        [sys.executable, "scripts/render_runtime_domain.py"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def collect_references() -> dict[str, list[tuple[str, str, str]]]:
    refs: dict[str, list[tuple[str, str, str]]] = {
        "actions": [],
        "collect_slots": [],
        "intents": [],
    }

    for path in iter_yaml_files(DATA_DIR):
        data = load_yaml(path)
        rel = str(path.relative_to(ROOT))

        for flow_id, flow in (data.get("flows") or {}).items():
            for step in flow.get("steps") or []:
                if not isinstance(step, dict):
                    continue
                if "action" in step:
                    refs["actions"].append((rel, str(flow_id), str(step["action"])))
                if "collect" in step:
                    refs["collect_slots"].append((rel, str(flow_id), str(step["collect"])))
                if "intent" in step:
                    refs["intents"].append((rel, str(flow_id), str(step["intent"])))

        for block_name in ("rules", "stories"):
            for block in data.get(block_name) or []:
                name = str(block.get("rule") or block.get("story") or block_name)
                for step in block.get("steps") or []:
                    if not isinstance(step, dict):
                        continue
                    if "action" in step:
                        refs["actions"].append((rel, name, str(step["action"])))
                    if "intent" in step:
                        refs["intents"].append((rel, name, str(step["intent"])))

    return refs


def collect_nlu_counts() -> tuple[Counter[str], dict[str, list[str]]]:
    counts: Counter[str] = Counter()
    locations: dict[str, list[str]] = defaultdict(list)

    for path in iter_yaml_files(DATA_DIR):
        data = load_yaml(path)
        rel = str(path.relative_to(ROOT))

        for item in data.get("nlu") or []:
            intent = item.get("intent")
            if not intent:
                continue

            examples = item.get("examples") or ""
            count = sum(
                1
                for line in str(examples).splitlines()
                if line.strip().startswith("-")
            )

            counts[str(intent)] += count
            locations[str(intent)].append(rel)

    return counts, locations


def collect_implemented_action_names() -> set[str]:
    """Statically collect custom action names returned by def name()."""
    names: set[str] = set()

    actions_dir = ROOT / "actions"
    if not actions_dir.exists():
        return names

    for path in sorted(actions_dir.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            raise RuntimeError(
                f"Python syntax error in {path.relative_to(ROOT)}: {exc}"
            ) from exc

        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue

            for child in node.body:
                if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                if child.name != "name":
                    continue

                for sub in ast.walk(child):
                    if (
                        isinstance(sub, ast.Return)
                        and isinstance(sub.value, ast.Constant)
                        and isinstance(sub.value.value, str)
                    ):
                        names.add(sub.value.value)

    return names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail on weak NLU warnings as well",
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    try:
        render_runtime()
    except subprocess.CalledProcessError as exc:
        print(exc.stdout or "", end="")
        print(exc.stderr or "", end="", file=sys.stderr)
        print("[fail] runtime render failed", file=sys.stderr)
        return 1

    domain_src = load_yaml(DOMAIN_SOURCE)
    domain = load_yaml(DOMAIN_GENERATED)

    for include in domain_src.get("includes") or []:
        inc_path = ROOT / str(include)
        if not inc_path.exists():
            errors.append(f"domain include missing: {include}")

    for path in iter_yaml_files(DATA_DIR):
        data = load_yaml(path)
        bad_keys = sorted(DOMAIN_ONLY_KEYS.intersection(data.keys()))
        if bad_keys:
            errors.append(
                f"{path.relative_to(ROOT)} contains domain-only keys {bad_keys}; "
                "move them to domain/*.yml"
            )

    intents = as_intent_set(domain.get("intents") or [])
    slots = set((domain.get("slots") or {}).keys())
    responses = set((domain.get("responses") or {}).keys())
    custom_actions = set(domain.get("actions") or [])
    implemented_actions = collect_implemented_action_names()

    for name in sorted(custom_actions - implemented_actions):
        warnings.append(f"domain action has no local Python implementation: {name}")

    refs = collect_references()

    used_actions = {name for _, _, name in refs["actions"]}
    used_utters = {name for name in used_actions if name.startswith("utter_")}
    used_custom = {
        name
        for name in used_actions
        if not name.startswith("utter_") and name not in {"action_listen"}
    }
    used_slots = {name for _, _, name in refs["collect_slots"]}
    used_intents = {name for _, _, name in refs["intents"]}

    for name in sorted(used_utters - responses):
        locs = [
            f"{f}:{flow}"
            for f, flow, action in refs["actions"]
            if action == name
        ][:3]
        errors.append(
            f"response missing in domain: {name} used at {', '.join(locs)}"
        )

    for name in sorted(used_custom - custom_actions):
        locs = [
            f"{f}:{flow}"
            for f, flow, action in refs["actions"]
            if action == name
        ][:3]
        errors.append(
            f"custom action missing in domain actions: {name} used at {', '.join(locs)}"
        )

    for name in sorted(used_slots - slots):
        locs = [
            f"{f}:{flow}"
            for f, flow, slot in refs["collect_slots"]
            if slot == name
        ][:3]
        errors.append(
            f"collect slot missing in domain slots: {name} used at {', '.join(locs)}"
        )

    for name in sorted(used_intents - intents):
        locs = [
            f"{f}:{flow}"
            for f, flow, intent in refs["intents"]
            if intent == name
        ][:3]
        errors.append(
            f"intent missing in domain intents: {name} used at {', '.join(locs)}"
        )

    nlu_counts, nlu_locations = collect_nlu_counts()

    missing_nlu = sorted(
        i for i in intents
        if i not in nlu_counts and i not in {"session_start"}
    )
    for name in missing_nlu:
        warnings.append(f"intent has no NLU examples: {name}")

    weak_nlu = sorted((name, count) for name, count in nlu_counts.items() if count < 5)
    for name, count in weak_nlu:
        warnings.append(f"intent has weak NLU coverage: {name} ({count} examples)")

    duplicates = {
        name: locs
        for name, locs in nlu_locations.items()
        if len(locs) > 1
    }
    for name, locs in sorted(duplicates.items()):
        uniq = sorted(set(locs))
        warnings.append(
            f"intent split across multiple NLU blocks: {name} -> {', '.join(uniq)}"
        )

    print("AzaBot training audit")
    print("====================")
    print(f"domain intents : {len(intents)}")
    print(f"domain slots   : {len(slots)}")
    print(f"responses      : {len(responses)}")
    print(f"custom actions : {len(custom_actions)}")
    print(f"implemented    : {len(implemented_actions)}")
    print(f"used actions   : {len(used_actions)}")
    print(f"nlu intents    : {len(nlu_counts)}")
    print("")

    if warnings:
        print("Warnings")
        print("--------")
        for warning in warnings:
            print(f"[warn] {warning}")
        print("")

    if errors or (args.strict and warnings):
        print("Errors")
        print("------")
        for error in errors:
            print(f"[error] {error}")

        if args.strict:
            for warning in warnings:
                print(f"[strict] {warning}")

        return 1

    print("[ok] training data audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())