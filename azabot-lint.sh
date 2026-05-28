#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  azabot-lint.sh — فحص وإصلاح شامل لكود AzaBot
#  الاستخدام:
#    bash azabot-lint.sh           ← فحص + إصلاح تلقائي
#    bash azabot-lint.sh --check   ← فحص فقط بدون إصلاح
#    bash azabot-lint.sh --report  ← تقرير مفصل فقط
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# ── CLI ───────────────────────────────────────────────────────
MODE="fix"
for arg in "$@"; do
  case "$arg" in
    --check)  MODE="check"  ;;
    --report) MODE="report" ;;
  esac
done

# ── ألوان ─────────────────────────────────────────────────────
G=$'\033[1;32m'; R=$'\033[1;31m'; Y=$'\033[1;33m'
C=$'\033[1;36m'; B=$'\033[1m';   D=$'\033[0;90m'; N=$'\033[0m'

# ── سجلات ─────────────────────────────────────────────────────
TS=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="$ROOT/reports"
REPORT_FILE="$REPORT_DIR/lint_${TS}.txt"
mkdir -p "$REPORT_DIR"

PASS=0; FAIL=0; FIXED=0; WARN=0
declare -a UNFIXED=()

# ── helpers ───────────────────────────────────────────────────
pass()  {
  PASS=$((PASS+1))
  printf "  ${G}✅ PASS${N}  %s\n" "$*"
  echo "PASS: $*" >> "$REPORT_FILE"
}
fail()  {
  FAIL=$((FAIL+1))
  printf "  ${R}❌ FAIL${N}  %s\n" "$*"
  echo "FAIL: $*" >> "$REPORT_FILE"
  UNFIXED+=("$*")
}
fixed() {
  FIXED=$((FIXED+1))
  printf "  ${C}🔧 FIXED${N} %s\n" "$*"
  echo "FIXED: $*" >> "$REPORT_FILE"
  # إزالة من UNFIXED إذا كان موجوداً
  local new=()
  for item in "${UNFIXED[@]:-}"; do
    [[ "$item" != *"${1%%:*}"* ]] && new+=("$item")
  done
  UNFIXED=("${new[@]:-}")
}
warn()  {
  WARN=$((WARN+1))
  printf "  ${Y}⚠️  WARN${N}  %s\n" "$*"
  echo "WARN: $*" >> "$REPORT_FILE"
}
info()  { printf "  ${D}ℹ  %s${N}\n" "$*"; }
section(){ printf "\n${B}${C}▶  %s${N}\n  %s\n" "$1" "$(printf '─%.0s' {1..55})"; echo "" >> "$REPORT_FILE"; echo "=== $1 ===" >> "$REPORT_FILE"; }
can_fix(){ [[ "$MODE" == "fix" ]]; }

# ══════════════════════════════════════════════════════════════
# 1. YAML FILES
# ══════════════════════════════════════════════════════════════
section "1/6  YAML — صحة البنية والمحتوى"

PYTHON_BIN="${ROOT}/.venv/bin/python"
[[ ! -f "$PYTHON_BIN" ]] && PYTHON_BIN="python3"

# تصدير وضع التشغيل لسكريبت بايثون الداخلي
export AZABOT_MODE="$MODE"

# فحص YAML
while IFS= read -r line; do
  case "$line" in
    YAML_OK:*)          pass "YAML سليم: ${line#YAML_OK: }" ;;
    YAML_ERR:*)         fail "خطأ في YAML: ${line#YAML_ERR: }" ;;
    YAML_FIXED_ALIAS:*) fixed "إصلاح alias عربي: ${line#YAML_FIXED_ALIAS: }" ;;
    YAML_FIXED_SLOTS:*) fixed "تحديث slots: ${line#YAML_FIXED_SLOTS: }" ;;
    YAML_WARN_SLOTS:*)  warn "slots قديمة: ${line#YAML_WARN_SLOTS: }" ;;
    YAML_DUP_RESP:*)    warn "رد مكرر: ${line#YAML_DUP_RESP: }" ;;
    NLU_DUP:*)          warn "مثال NLU مكرر: ${line#NLU_DUP: }" ;;
    FLOW_MISSING_STEP:*)fail "خطأ التدفق (Flows): ${line#FLOW_MISSING_STEP: }" ;;
    *)                  info "$line" ;;
  esac
done < <("$PYTHON_BIN" << 'PYEOF'
import yaml, re, sys, os
from pathlib import Path
from collections import defaultdict

ROOT = Path(os.environ.get("PWD", "."))
MODE = os.environ.get("AZABOT_MODE", "fix")
errors = []
warnings = []
fixed = []

# ── 1a. صحة YAML لكل الملفات ──────────────────────────────────
yaml_files = (
    list((ROOT/"data").rglob("*.yml")) +
    list((ROOT/"domain").glob("*.yml")) +
    [ROOT/"domain.yml", ROOT/"config.yml", ROOT/"endpoints.yml",
     ROOT/"endpoints.nodocker.yml", ROOT/"credentials.yml"]
)

for f in yaml_files:
    if not f.exists(): continue
    try:
        content = f.read_text(encoding="utf-8")
        # إصلاح: * في نص عربي يُفسَّر كـ YAML anchor
        fixed_content = content
        # أضف quotes حول النص المبدوء بـ *
        fixed_content = re.sub(
            r'^(\s+- text: \|.*?\n)((?:\s{6,}.*\n)*?\s{6,})\*([^\n]+)',
            lambda m: m.group(0),  # لا تغيّر — نتحقق فقط
            fixed_content, flags=re.MULTILINE
        )
        yaml.safe_load(content)
        print(f"YAML_OK: {f.relative_to(ROOT)}")
    except yaml.YAMLError as e:
        err_msg = str(e).split("\n")[0][:100]
        print(f"YAML_ERR: {f.relative_to(ROOT)} | {err_msg}")
        
        # محاولة إصلاح: * في نص عربي → نضع اقتباساً
        if MODE == "fix" and "alias" in str(e).lower():
            content = f.read_text(encoding="utf-8")
            # إصلاح *النص بإضافة مسافة قبلها أو إزالة *
            new_content = re.sub(r'(\s+\*)([\u0600-\u06FF])', r'\1 \2', content)
            if new_content != content:
                f.write_text(new_content, encoding="utf-8")
                print(f"YAML_FIXED_ALIAS: {f.relative_to(ROOT)}")

# ── 1b. Duplicate responses ────────────────────────────────────
all_responses = defaultdict(list)
for f in yaml_files:
    if not f.exists(): continue
    try:
        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for key in data.get("responses", {}):
            all_responses[key].append(str(f.relative_to(ROOT)))
    except: pass

dups = {k:v for k,v in all_responses.items() if len(v) > 1}
for resp, files in sorted(dups.items()):
    print(f"YAML_DUP_RESP: {resp} → {', '.join(files)}")

# ── 1c. custom slots deprecated → controlled ──────────────────
slot_files = list((ROOT/"domain").glob("*.yml")) + [ROOT/"domain.yml"]
for f in slot_files:
    if not f.exists(): continue
    content = f.read_text(encoding="utf-8")
    if "type: custom" in content:
        count = content.count("type: custom")
        if MODE == "fix":
            new_content = content.replace("type: custom", "type: controlled")
            f.write_text(new_content, encoding="utf-8")
            print(f"YAML_FIXED_SLOTS: {f.relative_to(ROOT)} | {count} custom→controlled")
        else:
            print(f"YAML_WARN_SLOTS: {f.relative_to(ROOT)} | {count} deprecated 'custom' slots")

# ── 1d. NLU examples متكررة بين intents ──────────────────────
nlu_examples = defaultdict(set)
nlu_files = list((ROOT/"data").rglob("nlu.yml"))
for f in nlu_files:
    try:
        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for item in data.get("nlu", []):
            intent = item.get("intent","")
            examples = item.get("examples","")
            if isinstance(examples, str):
                for line in examples.strip().split("\n"):
                    line = line.strip().lstrip("- ").strip()
                    if line:
                        nlu_examples[line].add(intent)
    except: pass

for example, intents in nlu_examples.items():
    if len(intents) > 1:
        print(f"NLU_DUP: '{example}' في: {', '.join(sorted(intents))}")

# ── 1e. Flow steps مفقودة ─────────────────────────────────────
flow_files = list((ROOT/"data").rglob("*.yml"))
for f in flow_files:
    try:
        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for fname, flow in (data.get("flows") or {}).items():
            steps = flow.get("steps", [])
            defined_ids = {"END","START"} | {s.get("id") for s in steps if isinstance(s,dict) and s.get("id")}
            for step in steps:
                if not isinstance(step, dict): continue
                nxt = step.get("next",[])
                targets = []
                if isinstance(nxt, str): targets = [nxt]
                elif isinstance(nxt, list):
                    for n in nxt:
                        if isinstance(n, dict):
                            t = n.get("then") or n.get("else","END")
                            if t: targets.append(t)
                for t in targets:
                    if t not in defined_ids:
                        print(f"FLOW_MISSING_STEP: {f.name}/{fname}: '{step.get('id','?')}' → '{t}' غير موجود")
    except: pass
PYEOF
)

# ══════════════════════════════════════════════════════════════
# 2. PYTHON ACTIONS (2/6)
# ══════════════════════════════════════════════════════════════
section "2/6  Python Actions — فحص الكود البرمجي (actions)"

if [ -d "actions" ]; then
    # التحقق من بناء الجملة (Syntax)
    for py_file in $(find actions -name "*.py"); do
        if "$PYTHON_BIN" -m py_compile "$py_file" 2>/dev/null; then
            pass "بناء الجملة سليم: $py_file"
        else
            fail "خطأ برمجي (Syntax Error) في: $py_file"
        fi
    done
    
    # التنسيق باستخدام black إذا كان متاحاً وفي وضع الإصلاح
    if can_fix && "$PYTHON_BIN" -m black --version >/dev/null 2>&1; then
        info "جاري التنسيق باستخدام black..."
        if "$PYTHON_BIN" -m black actions/ >/dev/null 2>&1; then
            fixed "تم تنسيق ملفات Python في مجلد actions/"
        else
            warn "مشكلة أثناء التنسيق باستخدام black"
        fi
    else
        info "تم تخطي التنسيق (black غير مثبت أو وضع الفحص فقط)."
    fi
else
    warn "مجلد actions/ غير موجود."
fi

# ══════════════════════════════════════════════════════════════
# 3. PROJECT STRUCTURE & FILES (3/6)
# ══════════════════════════════════════════════════════════════
section "3/6  هيكلية المشروع — فحص الملفات الأساسية"

REQUIRED_FILES=("config.yml" "domain.yml" "credentials.yml" "endpoints.yml")
for f in "${REQUIRED_FILES[@]}"; do
    if [ -f "$f" ]; then
        pass "الملف موجود: $f"
    else
        fail "الملف مفقود: $f"
    fi
done

if [ -d "data" ] && [ "$(ls -A data 2>/dev/null)" ]; then
    pass "مجلد data/ موجود ويحتوي على ملفات"
else
    fail "مجلد data/ غير موجود أو فارغ"
fi

# ══════════════════════════════════════════════════════════════
# 4. ENVIRONMENT VARIABLES (.env) (4/6)
# ══════════════════════════════════════════════════════════════
section "4/6  Environment Variables — إعدادات البيئة"

if [ -f ".env" ]; then
    pass "ملف .env موجود."
    # البحث عن أخطاء شائعة في .env مثل مسافات حول =
    if grep -q -E "^[A-Za-z0-9_]+\s+=" .env || grep -q -E "^[A-Za-z0-9_]+=\s+" .env; then
        fail "هناك مسافات غير صحيحة حول علامة '=' في ملف .env"
        if can_fix; then
            sed -i -E 's/^([A-Za-z0-9_]+)\s*=\s*(.*)/\1=\2/' .env
            fixed "تم إصلاح المسافات في ملف .env"
        fi
    else
        pass "تنسيق ملف .env سليم."
    fi
else
    warn "ملف .env غير موجود. قد يكون مطلوباً للتشغيل."
    if can_fix && [ -f ".env.example" ]; then
        cp .env.example .env
        fixed "تم إنشاء ملف .env من .env.example"
    fi
fi

# ══════════════════════════════════════════════════════════════
# 5. RASA DATA VALIDATE (5/6)
# ══════════════════════════════════════════════════════════════
section "5/6  Rasa Validator — فحص التوافق بين التدريب والنطاق"

validate_rasa() {
    local cmd=("$@")
    info "جاري تشغيل rasa data validate... (قد يستغرق بعض الوقت)"
    if "${cmd[@]}" data validate --fail-on-warnings > "$REPORT_DIR/rasa_validate.log" 2>&1; then
        pass "بيانات التدريب صالحة ومتوافقة (Rasa Validate)."
    else
        fail "تحذيرات أو أخطاء في بيانات Rasa (انظر التقرير: $REPORT_DIR/rasa_validate.log)."
    fi
}

if command -v rasa >/dev/null 2>&1; then
    validate_rasa rasa
elif [ -f "$PYTHON_BIN" ] && "$PYTHON_BIN" -m rasa --version >/dev/null 2>&1; then
    validate_rasa "$PYTHON_BIN" -m rasa
else
    warn "تعذر العثور على Rasa مثبتًا. تم تخطي فحص Validation."
fi

# ══════════════════════════════════════════════════════════════
# 6. REPORT SUMMARY (6/6)
# ══════════════════════════════════════════════════════════════
section "6/6  التقرير النهائي"

echo "==========================================" >> "$REPORT_FILE"
echo "النتيجة النهائية:" >> "$REPORT_FILE"
echo "  PASS:  $PASS" >> "$REPORT_FILE"
echo "  FAIL:  $FAIL" >> "$REPORT_FILE"
echo "  FIXED: $FIXED" >> "$REPORT_FILE"
echo "  WARN:  $WARN" >> "$REPORT_FILE"
echo "==========================================" >> "$REPORT_FILE"

printf "\n  ${B}إحصائيات الفحص:${N}\n"
printf "  ${G}✅ PASS:  %s${N}\n" "$PASS"
printf "  ${R}❌ FAIL:  %s${N}\n" "$FAIL"
printf "  ${C}🔧 FIXED: %s${N}\n" "$FIXED"
printf "  ${Y}⚠️  WARN:  %s${N}\n" "$WARN"

if [ ${#UNFIXED[@]} -gt 0 ]; then
    printf "\n  ${R}مشاكل تتطلب تدخلاً يدوياً:${N}\n"
    for item in "${UNFIXED[@]}"; do
        printf "    - %s\n" "$item"
    done
fi

printf "\n  ${D}تم حفظ التقرير المفصل في: %s${N}\n\n" "$REPORT_FILE"

if [ "$FAIL" -gt 0 ]; then
    exit 1
else
    exit 0
fi
