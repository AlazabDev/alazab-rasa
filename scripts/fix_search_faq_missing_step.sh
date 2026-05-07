#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(pwd)"
TS="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$ROOT/_repair_backups/fix_search_faq_missing_step_$TS"
REPORT_DIR="$ROOT/_repair_reports/fix_search_faq_missing_step_$TS"

mkdir -p "$BACKUP_DIR" "$REPORT_DIR"

echo "===== FIX RASA FLOW MISSING STEP ====="
echo "ROOT: $ROOT"
echo "BACKUP: $BACKUP_DIR"
echo "REPORT: $REPORT_DIR"

if [ ! -d "$ROOT/data" ]; then
  echo "ERROR: data directory not found. Run from Rasa project root."
  exit 1
fi

if [ ! -f "$ROOT/domain.yml" ] && [ ! -d "$ROOT/domain" ]; then
  echo "ERROR: domain.yml/domain directory not found."
  exit 1
fi

PYTHON_BIN="python"
if [ -x "$ROOT/.venv/bin/python" ]; then
  PYTHON_BIN="$ROOT/.venv/bin/python"
fi

"$PYTHON_BIN" - <<'PY'
from pathlib import Path
import re
import shutil
import json
import sys

root = Path.cwd()
backup_dir = root / "_repair_backups" / sorted((root / "_repair_backups").iterdir())[-1].name
report_dir = root / "_repair_reports" / sorted((root / "_repair_reports").iterdir())[-1].name

changes = []
errors = []

def is_skip(path: Path) -> bool:
    skip = {".git", ".venv", "venv", "env", "models", "__pycache__", "_repair_backups", "_repair_reports"}
    return bool(set(path.relative_to(root).parts) & skip)

def backup(path: Path):
    rel = path.relative_to(root)
    dst = backup_dir / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dst)

# 1) Locate flow file
flow_files = []
for path in list(root.rglob("*.yml")) + list(root.rglob("*.yaml")):
    if is_skip(path):
        continue
    try:
        txt = path.read_text(encoding="utf-8")
    except Exception:
        continue
    if "search_faq_by_keyword" in txt and "show_search_results" in txt:
        flow_files.append(path)

if not flow_files:
    errors.append("No YAML file found containing search_faq_by_keyword + show_search_results.")
else:
    target = flow_files[0]
    txt = target.read_text(encoding="utf-8")
    backup(target)

    if re.search(r"(?m)^\s*-\s*id:\s*ask_if_more_faqs\s*$", txt):
        changes.append(f"No flow patch needed. ask_if_more_faqs already exists in {target.relative_to(root)}")
    else:
        lines = txt.splitlines()
        show_idx = None
        show_indent = None

        for i, line in enumerate(lines):
            m = re.match(r"^(\s*)-\s*id:\s*show_search_results\s*$", line)
            if m:
                show_idx = i
                show_indent = m.group(1)
                break

        if show_idx is None:
            errors.append(f"Found flow file but could not locate exact step '- id: show_search_results' in {target.relative_to(root)}")
        else:
            insert_at = show_idx + 1

            while insert_at < len(lines):
                line = lines[insert_at]
                if re.match(rf"^{re.escape(show_indent)}-\s*id:\s*", line):
                    break
                if line.strip() and (len(line) - len(line.lstrip(" "))) < len(show_indent):
                    break
                insert_at += 1

            new_step = [
                f"{show_indent}- id: ask_if_more_faqs",
                f"{show_indent}  action: utter_ask_if_more_faqs"
            ]

            lines[insert_at:insert_at] = new_step
            target.write_text("\n".join(lines) + "\n", encoding="utf-8")
            changes.append(f"Inserted missing step ask_if_more_faqs into {target.relative_to(root)}")

# 2) Ensure response exists in domain
all_domain_text = ""
domain_candidates = []

if (root / "domain.yml").exists():
    domain_candidates.append(root / "domain.yml")

if (root / "domain").exists():
    domain_candidates.extend(sorted((root / "domain").rglob("*.yml")))
    domain_candidates.extend(sorted((root / "domain").rglob("*.yaml")))

for path in domain_candidates:
    if is_skip(path):
        continue
    try:
        all_domain_text += "\n" + path.read_text(encoding="utf-8")
    except Exception:
        pass

if "utter_ask_if_more_faqs:" in all_domain_text:
    changes.append("No domain patch needed. utter_ask_if_more_faqs already exists.")
else:
    try:
        import yaml
    except Exception as e:
        errors.append(f"PyYAML import failed: {e}")
        yaml = None

    if yaml is not None:
        domain_path = root / "domain.yml"
        if not domain_path.exists():
            errors.append("domain.yml not found for safe response insertion.")
        else:
            backup(domain_path)
            data = yaml.safe_load(domain_path.read_text(encoding="utf-8")) or {}

            if not isinstance(data, dict):
                errors.append("domain.yml root is not a mapping.")
            else:
                responses = data.get("responses")
                if responses is None:
                    responses = {}
                    data["responses"] = responses

                if not isinstance(responses, dict):
                    errors.append("domain.yml responses is not a mapping.")
                else:
                    responses["utter_ask_if_more_faqs"] = [
                        {
                            "text": "هل تريد البحث عن سؤال آخر، أم تحتاج مساعدة في طلب مختلف؟"
                        }
                    ]

                    domain_path.write_text(
                        yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120),
                        encoding="utf-8"
                    )
                    changes.append("Added response utter_ask_if_more_faqs to domain.yml")

# 3) Write report
report = {
    "changes": changes,
    "errors": errors,
    "flow_files_found": [str(p.relative_to(root)) for p in flow_files],
}
(report_dir / "fix_search_faq_missing_step_report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("===== CHANGES =====")
for c in changes:
    print("-", c)
if not changes:
    print("- none")

print("===== ERRORS =====")
for e in errors:
    print("-", e)
if not errors:
    print("- none")

if errors:
    sys.exit(1)
PY

echo
echo "===== VERIFY PATCH LOCATIONS ====="
grep -RIn "search_faq_by_keyword\|show_search_results\|ask_if_more_faqs\|utter_ask_if_more_faqs" \
  data domain.yml domain 2>/dev/null || true

echo
echo "===== RASA DATA VALIDATE ====="
bash scripts/botctl.sh validate 2>/dev/null || rasa data validate --debug

echo
echo "DONE."
echo "Now run:"
echo "bash scripts/botctl.sh train"
