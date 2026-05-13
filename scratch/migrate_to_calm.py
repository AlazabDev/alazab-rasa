#!/usr/bin/env python3
"""
Professional Migration Script: alazab-rasa → rasa-calm-demo
Converts Rasa Classic (NLU/Stories/Rules) → Rasa CALM (Flows/LLM)
"""
import os, shutil, yaml, re
from pathlib import Path
from datetime import datetime

SRC = Path("/home/azab/azabot/alazab-rasa")
DST = Path("/home/azab/azabot/rasa-calm-demo")
BACKUP = Path(f"/home/azab/azabot/rasa-calm-demo-backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}")

# ── 1. Backup target project ──────────────────────────────────────────────────
def backup():
    print(f"📦 Backing up {DST} → {BACKUP}")
    shutil.copytree(DST, BACKUP, dirs_exist_ok=False)
    print(f"✅ Backup done: {BACKUP}")

# ── 2. Copy actions ────────────────────────────────────────────────────────────
def copy_actions():
    src_actions = SRC / "actions"
    dst_actions = DST / "actions"
    # Keep existing CALM actions, add alazab actions
    for f in src_actions.iterdir():
        if f.suffix == ".py" and f.name not in {"__init__.py"}:
            dest = dst_actions / f"alazab_{f.name}"
            shutil.copy2(f, dest)
            print(f"  📄 Action: {f.name} → alazab_{f.name}")

# ── 3. Merge domain responses into _shared.yml ────────────────────────────────
def merge_domain():
    src_domain = SRC / "domain" / "general.yml"
    dst_shared = DST / "domain" / "_shared.yml"

    src_data = yaml.safe_load(src_domain.read_text(encoding="utf-8")) or {}
    dst_data = yaml.safe_load(dst_shared.read_text(encoding="utf-8")) or {}

    src_responses = src_data.get("responses", {})
    dst_responses = dst_data.get("responses", {})

    added = 0
    for key, val in src_responses.items():
        if key not in dst_responses:
            dst_responses[key] = val
            added += 1

    dst_data["responses"] = dst_responses

    # Merge slots
    src_slots = src_data.get("slots", {})
    dst_slots = dst_data.get("slots", {})
    for k, v in src_slots.items():
        if k not in dst_slots:
            # CALM needs from_llm for LLM-driven slots, keep custom slots as-is
            dst_slots[k] = v
    dst_data["slots"] = dst_slots

    # Merge intents
    src_intents = src_data.get("intents", [])
    dst_intents = dst_data.get("intents", [])
    existing = set(i if isinstance(i, str) else list(i.keys())[0] for i in dst_intents)
    for intent in src_intents:
        name = intent if isinstance(intent, str) else list(intent.keys())[0]
        if name not in existing:
            dst_intents.append(intent)
    dst_data["intents"] = dst_intents

    dst_shared.write_text(
        yaml.safe_dump(dst_data, allow_unicode=True, sort_keys=False, width=1000),
        encoding="utf-8"
    )
    print(f"  ✅ Merged {added} responses, {len(src_slots)} slots, {len(src_intents)} intents into _shared.yml")

# ── 4. Convert Rules/Stories → CALM Flows ─────────────────────────────────────
def convert_rules_to_flows():
    rules_dir = SRC / "data" / "rules"
    output_dir = DST / "data" / "flows"
    output_dir.mkdir(parents=True, exist_ok=True)

    for rules_file in rules_dir.glob("*.yml"):
        data = yaml.safe_load(rules_file.read_text(encoding="utf-8")) or {}
        rules = data.get("rules", [])
        if not rules:
            continue

        flows = {"version": "3.1", "flows": {}}
        for rule in rules:
            name = rule.get("rule", "unnamed")
            steps = rule.get("steps", [])

            flow_id = re.sub(r"[^\w]", "_", name).lower()[:40]
            flow_steps = []

            first_intent = None
            for step in steps:
                if "intent" in step:
                    first_intent = step["intent"]
                elif "action" in step:
                    action = step["action"]
                    if action.startswith("utter_"):
                        flow_steps.append({"action": action})
                    elif action.endswith("_form"):
                        flow_steps.append({
                            "collect": action.replace("_form", ""),
                            "description": f"Collect data for {action}"
                        })
                    else:
                        flow_steps.append({"action": action})

            if not flow_steps:
                flow_steps = [{"action": "utter_ask_help"}]

            flows["flows"][flow_id] = {
                "description": name,
                "nlu_trigger": [{"intent": first_intent}] if first_intent else [],
                "steps": flow_steps or [{"action": "utter_ask_help"}]
            }

        out_file = output_dir / f"alazab_{rules_file.stem}.yml"
        out_file.write_text(
            yaml.safe_dump(flows, allow_unicode=True, sort_keys=False, width=1000),
            encoding="utf-8"
        )
        print(f"  🔄 Converted {len(rules)} rules → {out_file.name}")

# ── 5. Copy NLU training data ─────────────────────────────────────────────────
def copy_nlu():
    dst_nlu_dir = DST / "data" / "nlu-based"
    dst_nlu_dir.mkdir(parents=True, exist_ok=True)

    for nlu_file in (SRC / "data" / "nlu").glob("*.yml"):
        dest = dst_nlu_dir / f"alazab_{nlu_file.name}"
        shutil.copy2(nlu_file, dest)
        print(f"  📚 NLU: {nlu_file.name} → {dest.name}")

    for brands_nlu in (SRC / "data" / "brands").glob("nlu.yml"):
        dest = dst_nlu_dir / "alazab_brands_nlu.yml"
        shutil.copy2(brands_nlu, dest)
        print(f"  📚 NLU: brands/nlu.yml → {dest.name}")

# ── 6. Copy domain sub-files as alazab_*.yml ──────────────────────────────────
def copy_domain_files():
    dst_domain_dir = DST / "domain" / "alazab"
    dst_domain_dir.mkdir(parents=True, exist_ok=True)

    for yf in (SRC / "domain").glob("*.yml"):
        dest = dst_domain_dir / f"alazab_{yf.name}"
        shutil.copy2(yf, dest)
        print(f"  🗂️  Domain: {yf.name} → alazab/{dest.name}")

# ── 7. Copy .env (without overwrite) ─────────────────────────────────────────
def copy_env():
    src_env = SRC / ".env"
    dst_env = DST / ".env.alazab"
    if src_env.exists():
        shutil.copy2(src_env, dst_env)
        print(f"  🔑 .env copied → .env.alazab (won't overwrite main .env)")

# ── 8. Copy webhook & scripts ─────────────────────────────────────────────────
def copy_extras():
    for name in ["webhook", "scripts"]:
        src_dir = SRC / name
        dst_dir = DST / name
        if src_dir.exists():
            if not dst_dir.exists():
                shutil.copytree(src_dir, dst_dir)
                print(f"  📁 Copied /{name}")
            else:
                # Merge without overwriting
                for f in src_dir.rglob("*"):
                    if f.is_file():
                        rel = f.relative_to(src_dir)
                        target = dst_dir / rel
                        if not target.exists():
                            target.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(f, target)
                print(f"  📁 Merged new files into /{name}")

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Starting Professional Migration: alazab-rasa → rasa-calm-demo")
    print("=" * 65)

    print("\n[1/7] Backup...")
    backup()

    print("\n[2/7] Copying Actions...")
    copy_actions()

    print("\n[3/7] Merging Domain (responses, slots, intents)...")
    merge_domain()

    print("\n[4/7] Converting Rules → CALM Flows...")
    convert_rules_to_flows()

    print("\n[5/7] Copying NLU training data...")
    copy_nlu()

    print("\n[6/7] Copying Domain sub-files...")
    copy_domain_files()

    print("\n[7/7] Copying .env & extras...")
    copy_env()
    copy_extras()

    print("\n" + "=" * 65)
    print("✅ Migration Complete!")
    print(f"   Source  : {SRC}")
    print(f"   Target  : {DST}")
    print(f"   Backup  : {BACKUP}")
    print("\nNext steps:")
    print("  1. cd /home/azab/azabot/rasa-calm-demo")
    print("  2. Review domain/_shared.yml for conflicts")
    print("  3. Review data/flows/alazab_*.yml flows")
    print("  4. Run: rasa data validate")
    print("  5. Run: rasa train")
