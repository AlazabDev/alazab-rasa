#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="$(pwd)"
TS="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$PROJECT_ROOT/_repair_backups/$TS"
REPORT_DIR="$PROJECT_ROOT/_repair_reports/$TS"
REPORT_FILE="$REPORT_DIR/repair_report.md"

mkdir -p "$BACKUP_DIR" "$REPORT_DIR"

echo "===== RASA WSL REPAIR ====="
echo "PROJECT_ROOT: $PROJECT_ROOT"
echo "BACKUP_DIR:   $BACKUP_DIR"
echo "REPORT_DIR:   $REPORT_DIR"

if [ ! -f "$PROJECT_ROOT/domain.yml" ]; then
  echo "ERROR: domain.yml not found. Run this script from Rasa project root."
  exit 1
fi

if [ ! -f "$PROJECT_ROOT/config.yml" ]; then
  echo "ERROR: config.yml not found. Run this script from Rasa project root."
  exit 1
fi

if [ ! -d "$PROJECT_ROOT/data" ]; then
  echo "ERROR: data directory not found. Run this script from Rasa project root."
  exit 1
fi

echo
echo "===== 1) BACKUP IMPORTANT FILES ====="

for p in \
  "domain.yml" \
  "config.yml" \
  "credentials.yml" \
  "endpoints.yml" \
  "data" \
  "actions" \
  "tests"
do
  if [ -e "$PROJECT_ROOT/$p" ]; then
    mkdir -p "$BACKUP_DIR/$(dirname "$p")"
    cp -a "$PROJECT_ROOT/$p" "$BACKUP_DIR/$p"
    echo "Backed up: $p"
  fi
done

echo
echo "===== 2) DETECT PYTHON ====="

PYTHON_BIN="python3"

if [ -x "$PROJECT_ROOT/.venv/bin/python" ]; then
  PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"
elif [ -n "${VIRTUAL_ENV:-}" ] && [ -x "$VIRTUAL_ENV/bin/python" ]; then
  PYTHON_BIN="$VIRTUAL_ENV/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "ERROR: python3 not found."
  exit 1
fi

echo "PYTHON_BIN: $PYTHON_BIN"
"$PYTHON_BIN" --version

echo
echo "===== 3) SAFE TEXT NORMALIZATION ====="

"$PYTHON_BIN" - <<'PY'
from pathlib import Path

root = Path.cwd()
target_exts = {".yml", ".yaml", ".json", ".jsonl", ".md", ".txt", ".py"}
skip_dirs = {
    ".git", ".venv", "venv", "env",
    "__pycache__", ".mypy_cache", ".pytest_cache",
    "_repair_backups", "_repair_reports", "models"
}

changed = []

for path in root.rglob("*"):
    if not path.is_file():
        continue

    rel_parts = set(path.relative_to(root).parts)
    if rel_parts & skip_dirs:
        continue

    if path.suffix.lower() not in target_exts:
        continue

    try:
        raw = path.read_bytes()
    except Exception:
        continue

    original = raw

    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]

    text = raw.decode("utf-8", errors="replace")
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    if path.suffix.lower() in {".yml", ".yaml"}:
        fixed_lines = []
        for line in text.split("\n"):
            leading_tabs = len(line) - len(line.lstrip("\t"))
            if leading_tabs:
                line = ("  " * leading_tabs) + line.lstrip("\t")
            fixed_lines.append(line.rstrip())
        text = "\n".join(fixed_lines)
    elif path.suffix.lower() == ".py":
        text = "\n".join(line.rstrip() for line in text.split("\n"))

    if text and not text.endswith("\n"):
        text += "\n"

    new = text.encode("utf-8")

    if new != original:
        path.write_bytes(new)
        changed.append(str(path.relative_to(root)))

print("Normalized files:")
if changed:
    for item in changed:
        print(f"- {item}")
else:
    print("- none")
PY

echo
echo "===== 4) STRUCTURE + YAML/JSON REPAIR ====="

"$PYTHON_BIN" - <<'PY'
from pathlib import Path
import json
import sys

root = Path.cwd()
report = []
errors = []

try:
    import yaml
except Exception as e:
    print("ERROR: PyYAML is not available in the current Python environment.")
    print("Activate your Rasa venv first, then rerun.")
    sys.exit(1)

def read_yaml(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data if data is not None else {}
    except Exception as e:
        errors.append({"file": str(path.relative_to(root)), "type": "YAML_ERROR", "error": str(e)})
        return None

def write_yaml(path: Path, data):
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=120)

def unique_keep_order(items):
    out = []
    seen = set()
    for item in items or []:
        if item is None:
            continue
        key = json.dumps(item, ensure_ascii=False, sort_keys=True) if not isinstance(item, str) else item
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out

domain_path = root / "domain.yml"
domain = read_yaml(domain_path)

if not isinstance(domain, dict):
    errors.append({"file": "domain.yml", "type": "DOMAIN_ERROR", "error": "domain.yml root must be a mapping/object"})
    domain = {}

required_domain_keys = {
    "version": "3.1",
    "intents": [],
    "entities": [],
    "slots": {},
    "responses": {},
    "actions": [],
    "session_config": {
        "session_expiration_time": 60,
        "carry_over_slots_to_new_session": True
    }
}

for key, default in required_domain_keys.items():
    if key not in domain or domain[key] is None:
        domain[key] = default
        report.append(f"Added missing domain key: {key}")

if str(domain.get("version", "")).strip() == "":
    domain["version"] = "3.1"
    report.append("Fixed empty domain version")

if not isinstance(domain.get("intents"), list):
    domain["intents"] = []
    report.append("Fixed domain intents to list")

if not isinstance(domain.get("entities"), list):
    domain["entities"] = []
    report.append("Fixed domain entities to list")

if not isinstance(domain.get("slots"), dict):
    domain["slots"] = {}
    report.append("Fixed domain slots to dict")

if not isinstance(domain.get("responses"), dict):
    domain["responses"] = {}
    report.append("Fixed domain responses to dict")

if not isinstance(domain.get("actions"), list):
    domain["actions"] = []
    report.append("Fixed domain actions to list")

domain["intents"] = unique_keep_order(domain["intents"])
domain["entities"] = unique_keep_order(domain["entities"])
domain["actions"] = unique_keep_order(domain["actions"])

nlu_intents = set()
story_rule_actions = set()
utter_refs = set()

for yml in sorted((root / "data").rglob("*.yml")) + sorted((root / "data").rglob("*.yaml")):
    data = read_yaml(yml)
    if data is None:
        continue

    if not isinstance(data, dict):
        errors.append({"file": str(yml.relative_to(root)), "type": "DATA_FORMAT", "error": "YAML root must be mapping/object"})
        continue

    if "version" not in data:
        data = {"version": "3.1", **data}
        write_yaml(yml, data)
        report.append(f"Added version to {yml.relative_to(root)}")

    for item in data.get("nlu", []) or []:
        if isinstance(item, dict) and item.get("intent"):
            nlu_intents.add(item["intent"])

    for section in ("stories", "rules"):
        for block in data.get(section, []) or []:
            if not isinstance(block, dict):
                continue
            for step in block.get("steps", []) or []:
                if not isinstance(step, dict):
                    continue
                action = step.get("action")
                if action:
                    story_rule_actions.add(action)
                    if str(action).startswith("utter_"):
                        utter_refs.add(action)

missing_intents = sorted(i for i in nlu_intents if i not in domain["intents"])
if missing_intents:
    domain["intents"].extend(missing_intents)
    domain["intents"] = unique_keep_order(domain["intents"])
    report.append(f"Added missing intents to domain: {', '.join(missing_intents)}")

builtin_actions = {
    "action_listen", "action_restart", "action_session_start", "action_default_fallback",
    "action_deactivate_loop", "action_revert_fallback_events", "action_two_stage_fallback",
    "action_default_ask_affirmation", "action_default_ask_rephrase", "action_back",
    "action_unlikely_intent", "action_extract_slots"
}

custom_actions = sorted(
    a for a in story_rule_actions
    if not str(a).startswith("utter_") and a not in builtin_actions
)

missing_actions = [a for a in custom_actions if a not in domain["actions"]]
if missing_actions:
    domain["actions"].extend(missing_actions)
    domain["actions"] = unique_keep_order(domain["actions"])
    report.append(f"Added missing custom actions to domain: {', '.join(missing_actions)}")

missing_responses = sorted(u for u in utter_refs if u not in domain["responses"])
if missing_responses:
    for u in missing_responses:
        domain["responses"][u] = [{"text": "تم استلام طلبك. من فضلك أرسل التفاصيل المطلوبة لاستكمال الإجراء."}]
    report.append(f"Added placeholder responses for missing utter refs: {', '.join(missing_responses)}")

write_yaml(domain_path, domain)

for json_file in sorted(root.rglob("*.json")):
    if any(part in {".venv", "venv", "env", ".git", "_repair_backups", "_repair_reports", "models"} for part in json_file.parts):
        continue
    try:
        json.loads(json_file.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append({"file": str(json_file.relative_to(root)), "type": "JSON_ERROR", "error": str(e)})

for jsonl_file in sorted(root.rglob("*.jsonl")):
    if any(part in {".venv", "venv", "env", ".git", "_repair_backups", "_repair_reports", "models"} for part in jsonl_file.parts):
        continue
    for idx, line in enumerate(jsonl_file.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            json.loads(line)
        except Exception as e:
            errors.append({"file": str(jsonl_file.relative_to(root)), "type": "JSONL_ERROR", "line": idx, "error": str(e)})

out_dir = root / "_repair_reports" / sorted((root / "_repair_reports").iterdir())[-1].name
(out_dir / "structure_repair.json").write_text(
    json.dumps({"changes": report, "errors": errors}, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("Changes:")
for r in report:
    print(f"- {r}")
if not report:
    print("- none")

print("Errors:")
for e in errors:
    print(f"- {e}")
if not errors:
    print("- none")
PY

echo
echo "===== 5) PYTHON ACTIONS COMPILE CHECK ====="

if [ -d "$PROJECT_ROOT/actions" ]; then
  "$PYTHON_BIN" -m compileall -q "$PROJECT_ROOT/actions" || true
else
  echo "No actions directory."
fi

echo
echo "===== 6) RASA VALIDATION ====="

RASA_CMD=""

if [ -x "$PROJECT_ROOT/.venv/bin/rasa" ]; then
  RASA_CMD="$PROJECT_ROOT/.venv/bin/rasa"
elif command -v rasa >/dev/null 2>&1; then
  RASA_CMD="$(command -v rasa)"
elif "$PYTHON_BIN" -m rasa --version >/dev/null 2>&1; then
  RASA_CMD="$PYTHON_BIN -m rasa"
fi

if [ -n "$RASA_CMD" ]; then
  echo "RASA_CMD: $RASA_CMD"
  set +e
  bash -lc "$RASA_CMD --version" | tee "$REPORT_DIR/rasa_version.txt"
  VALIDATE_OUTPUT="$(bash -lc "$RASA_CMD data validate --debug" 2>&1)"
  VALIDATE_CODE=$?
  set -e

  printf "%s\n" "$VALIDATE_OUTPUT" | tee "$REPORT_DIR/rasa_data_validate.log"

  if [ "$VALIDATE_CODE" -ne 0 ]; then
    echo "RASA_VALIDATE_STATUS=FAILED" | tee "$REPORT_DIR/rasa_validate_status.txt"
  else
    echo "RASA_VALIDATE_STATUS=PASS" | tee "$REPORT_DIR/rasa_validate_status.txt"
  fi
else
  echo "Rasa command not found. Activate .venv then rerun." | tee "$REPORT_DIR/rasa_validate_status.txt"
fi

echo
echo "===== 7) FINAL REPORT ====="

cat > "$REPORT_FILE" <<EOF
# Rasa WSL Repair Report

- Project root: $PROJECT_ROOT
- Backup dir: $BACKUP_DIR
- Report dir: $REPORT_DIR
- Python: $PYTHON_BIN

## What was repaired safely

- UTF-8 BOM removed when found.
- CRLF converted to LF.
- YAML leading tabs converted to spaces.
- Missing \`version: "3.1"\` added to data YAML files.
- Missing domain keys added if absent.
- Missing NLU intents added to domain.
- Missing custom actions referenced in stories/rules added to domain actions.
- Missing utter responses referenced in stories/rules added with safe placeholder text.
- JSON and JSONL syntax checked.
- Python action files compiled.

## Validation logs

- \`$REPORT_DIR/structure_repair.json\`
- \`$REPORT_DIR/rasa_data_validate.log\`
- \`$REPORT_DIR/rasa_validate_status.txt\`

EOF

echo "DONE."
echo "Report: $REPORT_FILE"
echo
echo "Send me:"
echo "$REPORT_DIR/rasa_validate_status.txt"
echo "$REPORT_DIR/rasa_data_validate.log"
