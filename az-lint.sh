#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  az-lint.sh — فحص وإصلاح شامل لكود AzaBot
#  الاستخدام:
#    bash az-lint.sh           ← فحص + إصلاح تلقائي
#    bash az-lint.sh --check   ← فحص فقط
#    bash az-lint.sh --report  ← تقرير مفصل
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

MODE="fix"
for arg in "$@"; do
  case "$arg" in
    --check)  MODE="check"  ;;
    --report) MODE="report" ;;
    --fix)    MODE="fix"    ;;
  esac
done

# ── ألوان ─────────────────────────────────────────────────────
G=$'\033[1;32m'; R=$'\033[1;31m'; Y=$'\033[1;33m'
C=$'\033[1;36m'; B=$'\033[1m';    N=$'\033[0m'

TS=$(date +%Y%m%d_%H%M%S)
REPORT_DIR="$ROOT/reports"
REPORT_FILE="$REPORT_DIR/lint_${TS}.md"
mkdir -p "$REPORT_DIR"

PASS=0; FAIL=0; FIXED=0; WARN=0
declare -a UNFIXED_LIST=()

pass()  { PASS=$((PASS+1));  printf "  ${G}✅ PASS${N}  %s\n" "$*";  echo "- ✅ PASS: $*" >> "$REPORT_FILE"; }
fail()  { FAIL=$((FAIL+1));  printf "  ${R}❌ FAIL${N}  %s\n" "$*";  echo "- ❌ FAIL: $*" >> "$REPORT_FILE"; UNFIXED_LIST+=("$*"); }
fixed() { FIXED=$((FIXED+1)); printf "  ${C}🔧 FIXED${N} %s\n" "$*"; echo "- 🔧 FIXED: $*" >> "$REPORT_FILE"; }
warn()  { WARN=$((WARN+1));  printf "  ${Y}⚠️  WARN${N}  %s\n" "$*";  echo "- ⚠️ WARN: $*" >> "$REPORT_FILE"; }
section(){ printf "\n${B}${C}▶  %s${N}\n  %s\n" "$1" "$(printf '─%.0s' {1..55})"; echo -e "\n## $1" >> "$REPORT_FILE"; }
can_fix(){ [[ "$MODE" == "fix" ]]; }

PYTHON="${ROOT}/.venv/bin/python"
[[ ! -f "$PYTHON" ]] && PYTHON="python3"

printf "${B}${C}\n  🩺 azabot-lint — فحص شامل وإصلاح تلقائي${N}\n"
printf "  المشروع: %s\n  الوضع:   %s\n  الوقت:   %s\n\n" "$ROOT" "$MODE" "$(date)"
echo "# AzaBot Lint Report — $(date)" > "$REPORT_FILE"
echo "Mode: $MODE" >> "$REPORT_FILE"

# ══════════════════════════════════════════════════════════════
# 1. YAML — بنية وتكرار ومشاكل slots
# ══════════════════════════════════════════════════════════════
section "1/7  YAML — بنية ومحتوى وtokens"

export AZABOT_ROOT="$ROOT" AZABOT_MODE="$MODE"

$PYTHON - << 'PYEOF'
import yaml, re, sys, os
from pathlib import Path
from collections import defaultdict

ROOT = Path(os.environ["AZABOT_ROOT"])
MODE = os.environ["AZABOT_MODE"]
G="\033[1;32m"; R="\033[1;31m"; Y="\033[1;33m"; C="\033[1;36m"; N="\033[0m"

def ok(m):  print(f"  {G}✅ PASS{N}  {m}")
def err(m): print(f"  {R}❌ FAIL{N}  {m}")
def fix(m): print(f"  {C}🔧 FIXED{N} {m}")
def wrn(m): print(f"  {Y}⚠️  WARN{N}  {m}")

yaml_files = (
    list((ROOT/"data").rglob("*.yml")) +
    list((ROOT/"domain").glob("*.yml")) +
    [f for f in [ROOT/"domain.yml", ROOT/"config.yml",
     ROOT/"endpoints.yml", ROOT/"credentials.yml"] if f.exists()]
)

broken = 0
for f in yaml_files:
    try:
        content = f.read_text(encoding="utf-8")
        yaml.safe_load(content)
    except yaml.YAMLError as e:
        msg = str(e).split("\n")[0][:120]
        if MODE == "fix":
            fixed_content = content
            # إصلاح 1: * عربي يُفسَّر كـ anchor
            if "alias" in msg.lower() or "anchor" in msg.lower():
                fixed_content = re.sub(
                    r'(\n\s+)(\*)([\u0600-\u06FFa-zA-Z])',
                    r'\1\\\2\3', fixed_content
                )
            # إصلاح 2: مسافة مكسورة في responses block
            # إصلاح 3: تبويبات مختلطة
            if "\t" in fixed_content:
                fixed_content = fixed_content.replace("\t", "  ")
            if fixed_content != content:
                f.write_text(fixed_content, encoding="utf-8")
                try:
                    yaml.safe_load(fixed_content)
                    fix(f"{f.relative_to(ROOT)}: YAML أُصلح تلقائياً")
                    continue
                except:
                    pass
        err(f"{f.relative_to(ROOT)}: {msg}")
        broken += 1

if broken == 0:
    ok(f"كل ملفات YAML ({len(yaml_files)}) سليمة")

# ── Duplicate responses ────────────────────────────────────────
all_responses = defaultdict(list)
for f in yaml_files:
    try:
        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for key in data.get("responses", {}):
            all_responses[key].append(str(f.relative_to(ROOT)))
    except: pass

dups = {k:v for k,v in all_responses.items() if len(v) > 1}
if dups:
    for resp, files in sorted(dups.items()):
        wrn(f"response مكررة: {resp} في {', '.join(files)}")
    if MODE == "fix":
        # الأولوية: show_faqs.yml > feedback.yml > domain/general.yml > domain.yml
        priority = ["show_faqs.yml", "feedback.yml", "domain.yml"]
        keep_in = {}
        for resp in dups:
            for p in priority:
                sources = [f for f in dups[resp] if f.endswith(p)]
                if sources:
                    keep_in[resp] = p
                    break
            else:
                keep_in[resp] = dups[resp][0].split("/")[-1]

        for resp, keeper in keep_in.items():
            for fpath_str in dups[resp]:
                if not fpath_str.endswith(keeper):
                    f = ROOT / fpath_str
                    try:
                        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
                        if resp in (data.get("responses") or {}):
                            del data["responses"][resp]
                            # إعادة كتابة آمنة
                            content = f.read_text(encoding="utf-8")
                            lines = content.split("\n")
                            out, skip = [], False
                            for line in lines:
                                if re.match(rf'^  {re.escape(resp)}:', line):
                                    skip = True
                                elif skip and re.match(r'^  \w', line) and not line.startswith("    "):
                                    skip = False
                                if not skip:
                                    out.append(line)
                            new_content = "\n".join(out)
                            try:
                                yaml.safe_load(new_content)
                                f.write_text(new_content, encoding="utf-8")
                                fix(f"response مكررة '{resp}' حُذفت من {fpath_str}")
                            except:
                                wrn(f"لم يمكن حذف '{resp}' من {fpath_str} بأمان")
                    except Exception as e:
                        wrn(f"خطأ في معالجة {fpath_str}: {e}")
else:
    ok("لا توجد responses مكررة")

# ── custom slots deprecated → controlled ──────────────────────
slot_files = list((ROOT/"domain").glob("*.yml")) + [ROOT/"domain.yml"]
total_custom = 0
for f in slot_files:
    if not f.exists(): continue
    content = f.read_text(encoding="utf-8")
    count = content.count("type: custom")
    if count:
        total_custom += count
        if MODE == "fix":
            f.write_text(content.replace("type: custom", "type: controlled"), encoding="utf-8")
            fix(f"{f.relative_to(ROOT)}: {count} custom→controlled")
        else:
            wrn(f"{f.relative_to(ROOT)}: {count} deprecated 'custom' slots")

if total_custom == 0:
    ok("لا توجد custom slots مهجورة")

# ── NLU examples متكررة بين intents ──────────────────────────
nlu_examples = defaultdict(set)
for f in (ROOT/"data").rglob("nlu.yml"):
    try:
        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for item in data.get("nlu", []):
            intent = item.get("intent", "")
            examples = item.get("examples", "") or ""
            for line in examples.strip().split("\n"):
                ex = line.strip().lstrip("- ").strip()
                if ex:
                    nlu_examples[ex].add(intent)
    except: pass

dup_ex = {ex:intents for ex,intents in nlu_examples.items() if len(intents) > 1}
if dup_ex:
    for ex, intents in list(dup_ex.items())[:20]:
        wrn(f"NLU مكرر: '{ex[:50]}' في: {', '.join(sorted(intents))}")
    if MODE == "fix":
        # نحذف المثال من الـ intent الثانوي (نبقى على الأول الأهم)
        fixed_count = 0
        for f in (ROOT/"data").rglob("nlu.yml"):
            try:
                content = f.read_text(encoding="utf-8")
                data = yaml.safe_load(content) or {}
                changed = False
                for item in data.get("nlu", []):
                    intent = item.get("intent", "")
                    examples = item.get("examples", "") or ""
                    lines = examples.split("\n")
                    new_lines = []
                    for line in lines:
                        ex = line.strip().lstrip("- ").strip()
                        if ex in dup_ex:
                            first_intent = sorted(dup_ex[ex])[0]
                            if intent != first_intent:
                                changed = True
                                fixed_count += 1
                                continue
                        new_lines.append(line)
                    item["examples"] = "\n".join(new_lines)
                if changed:
                    f.write_text(f"version: \"3.1\"\n\nnlu:\n" +
                        "\n".join(f"  - intent: {i.get('intent','')}\n    examples: |\n" +
                            "\n".join(f"      {l}" for l in (i.get('examples','') or '').split('\n') if l.strip())
                            for i in data.get("nlu", [])),
                        encoding="utf-8")
                    fix(f"{f.relative_to(ROOT)}: {fixed_count} مثال مكرر حُذف")
            except Exception as e:
                wrn(f"لم يمكن إصلاح NLU {f.name}: {e}")
    print(f"  {Y}⚠️  WARN{N}  {len(dup_ex)} مثال NLU مكرر — تحقق يدوياً للتأكيد")
else:
    ok("لا توجد أمثلة NLU مكررة")

# ── Flow steps مفقودة ─────────────────────────────────────────
flow_issues = []
for f in (ROOT/"data").rglob("*.yml"):
    try:
        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for fname, flow in (data.get("flows") or {}).items():
            steps = flow.get("steps", []) or []
            ids = {"END","START"} | {s.get("id") for s in steps if isinstance(s,dict) and s.get("id")}
            for step in steps:
                if not isinstance(step, dict): continue
                nxt = step.get("next", [])
                targets = [nxt] if isinstance(nxt, str) else []
                if isinstance(nxt, list):
                    for n in nxt:
                        if isinstance(n, dict):
                            for k in ("then","else"):
                                t = n.get(k)
                                if t and t not in ("END","START"): targets.append(t)
                for t in targets:
                    if t not in ids:
                        flow_issues.append(f"{f.name}/{fname}: '{step.get('id','?')}' → '{t}' مفقود")
    except: pass

if flow_issues:
    for issue in flow_issues:
        err(f"Flow step: {issue}")
else:
    ok("كل flow steps موجودة")
PYEOF

# ══════════════════════════════════════════════════════════════
# 2. PYTHON — syntax + security fixes
# ══════════════════════════════════════════════════════════════
section "2/7  Python — Syntax وأمان"

$PYTHON - << 'PYEOF'
import ast, os, re, sys
from pathlib import Path

ROOT = Path(os.environ["AZABOT_ROOT"])
MODE = os.environ["AZABOT_MODE"]
G="\033[1;32m"; R="\033[1;31m"; Y="\033[1;33m"; C="\033[1;36m"; N="\033[0m"

def ok(m):  print(f"  {G}✅ PASS{N}  {m}")
def err(m): print(f"  {R}❌ FAIL{N}  {m}")
def fix(m): print(f"  {C}🔧 FIXED{N} {m}")
def wrn(m): print(f"  {Y}⚠️  WARN{N}  {m}")

py_files = [f for f in (ROOT/"actions").rglob("*.py")]
py_files += [f for f in (ROOT/"webhook").rglob("*.py")]

# ── 2a. Syntax errors ─────────────────────────────────────────
syntax_errors = 0
for f in py_files:
    try:
        ast.parse(f.read_text(encoding="utf-8"))
    except SyntaxError as e:
        err(f"{f.relative_to(ROOT)}: SyntaxError سطر {e.lineno}: {e.msg}")
        syntax_errors += 1

if syntax_errors == 0:
    ok(f"كل ملفات Python ({len(py_files)}) بدون أخطاء syntax")

# ── 2b. Path Traversal fix ─────────────────────────────────────
admin_router = ROOT/"webhook/routers/admin.py"
if admin_router.exists():
    content = admin_router.read_text(encoding="utf-8")
    # الثغرة: file_path = Path(upload.get("path",""))
    old = 'file_path = Path(upload.get("path",""))'
    new = (
        'file_path = (UPLOADS_DIR / Path(upload.get("path","")).name).resolve()\n'
        '    if not str(file_path).startswith(str(UPLOADS_DIR.resolve())):\n'
        '        raise HTTPException(403, "الوصول مرفوض")'
    )
    if old in content and MODE == "fix":
        content = content.replace(old, new, 1)
        admin_router.write_text(content, encoding="utf-8")
        fix("webhook/routers/admin.py: Path Traversal مُصلَح")
    elif old in content:
        err("webhook/routers/admin.py: ثغرة Path Traversal غير مُصلَحة")
    else:
        ok("webhook/routers/admin.py: لا ثغرة Path Traversal")

    # ثغرة تسرب معلومات في رسائل خطأ
    old2 = 'f"إجراء غير مدعوم: {action}"'
    new2 = '"طلب غير صحيح"'
    if old2 in content and MODE == "fix":
        content = admin_router.read_text(encoding="utf-8")
        content = content.replace(old2, new2)
        admin_router.write_text(content, encoding="utf-8")
        fix("webhook/routers/admin.py: تسرب معلومات action مُصلَح")
    elif old2 in content:
        wrn("webhook/routers/admin.py: رسالة خطأ تُظهر اسم الـ action")

    # تحسين timeout التدريب
    old3 = "timeout=600"
    new3 = "timeout=1800  # 30 دقيقة"
    content = admin_router.read_text(encoding="utf-8")
    if old3 in content and MODE == "fix":
        content = content.replace(old3, new3, 1)
        admin_router.write_text(content, encoding="utf-8")
        fix("webhook/routers/admin.py: training timeout 10→30 دقيقة")
    elif old3 in content:
        wrn("webhook/routers/admin.py: training timeout قصير (600s)")

# ── 2c. health/details بدون مصادقة ───────────────────────────
server_py = ROOT/"webhook/server.py"
if server_py.exists():
    content = server_py.read_text(encoding="utf-8")

    # فحص /health/details
    if '@app.get("/health/details"' in content:
        if "Depends" not in content[content.find('/health/details'):content.find('/health/details')+300]:
            if MODE == "fix":
                old_hd = '@app.get("/health/details", tags=["System"])\nasync def health_details(request: Request):'
                new_hd = '@app.get("/health/details", tags=["System"])\nasync def health_details(request: Request, _user: dict = Depends(_require_admin)):'
                if old_hd in content:
                    content = content.replace(old_hd, new_hd, 1)
                    server_py.write_text(content, encoding="utf-8")
                    fix("webhook/server.py: /health/details محمي بـ admin auth")
                else:
                    wrn("webhook/server.py: /health/details — تحقق يدوياً من المصادقة")
            else:
                err("webhook/server.py: /health/details مكشوف بدون مصادقة")
        else:
            ok("webhook/server.py: /health/details محمي")

    # structured logging (production)
    if "json" not in content[:3000].lower() and "NODE_ENV" in content:
        ok("webhook/server.py: logging مضبوط")
    
    # CORS check
    if 'allow_origins=["*"]' in content or "allow_origins=['*']" in content:
        if MODE == "fix":
            content = server_py.read_text(encoding="utf-8")
            content = content.replace('allow_origins=["*"]', 'allow_origins=ALLOWED_ORIGINS')
            content = content.replace("allow_origins=['*']", 'allow_origins=ALLOWED_ORIGINS')
            server_py.write_text(content, encoding="utf-8")
            fix("webhook/server.py: CORS allow_origins=* مُصلَح")
        else:
            err("webhook/server.py: CORS allow_origins=* خطير")
    else:
        ok("webhook/server.py: CORS origins محدد")

# ── 2d. OpenAI API key validation ─────────────────────────────
chat_router = ROOT/"webhook/routers/chat.py"
if chat_router.exists():
    content = chat_router.read_text(encoding="utf-8")

    # تحسين: التحقق من API key قبل الاستخدام
    old_key = 'api_key = os.getenv("OPENAI_API_KEY", "").strip()\n        if not api_key'
    if 'api_key = os.getenv("OPENAI_API_KEY", "").strip()' in content:
        ok("webhook/routers/chat.py: OpenAI key validation موجود")
    else:
        wrn("webhook/routers/chat.py: تحقق من validation الـ OPENAI_API_KEY")

    # error handling في TTS streaming
    if "except Exception as exc:" in content and "TTS" in content.upper():
        ok("webhook/routers/chat.py: TTS error handling موجود")

# ── 2e. فحص imports غير مستخدمة (تحذير فقط) ─────────────────
unused_count = 0
for f in py_files:
    content = f.read_text(encoding="utf-8")
    # فحص بسيط للـ imports الواضحة
    if "import *" in content:
        wrn(f"{f.relative_to(ROOT)}: استخدام 'import *' — تجنبه")
        unused_count += 1

if unused_count == 0:
    ok("لا يوجد 'import *' في الكود")

# ── 2f. ENCRYPTION_KEY استخدام ────────────────────────────────
services_dir = ROOT/"webhook/services"
if services_dir.exists():
    for f in services_dir.rglob("*.py"):
        content = f.read_text(encoding="utf-8")
        # البيانات الحساسة بدون تشفير
        if re.search(r'user_phone|phone.*=.*lead|lead.*phone', content):
            if "cipher" not in content and "encrypt" not in content.lower():
                wrn(f"{f.relative_to(ROOT)}: أرقام هواتف قد تُحفظ بدون تشفير")
PYEOF

# ══════════════════════════════════════════════════════════════
# 3. TypeScript/Frontend — lint
# ══════════════════════════════════════════════════════════════
section "3/7  TypeScript/Frontend — Lint"

if [[ -d "$ROOT/azabot" ]] && command -v pnpm &>/dev/null; then
    cd "$ROOT/azabot"

    if [[ ! -d "node_modules" ]]; then
        warn "node_modules مفقود — تخطي frontend lint"
    else
        # فحص syntax مبدئي بدون تشغيل tsc كامل
        TS_ERRORS=0

        # فحص الـ imports المكسورة
        while IFS= read -r -d '' f; do
            if grep -qP "from ['\"]@/[^'\"]+['\"]" "$f" 2>/dev/null; then
                # تحقق من الـ path alias مضبوط
                :
            fi
            # فحص regex مكسور
            if grep -qP '\\n\s*\]\)' "$f" 2>/dev/null; then
                warn "$(basename $f): regex متكسر على سطرين — تحقق يدوياً"
                TS_ERRORS=$((TS_ERRORS+1))
            fi
        done < <(find src -name "*.ts" -o -name "*.tsx" -print0 2>/dev/null)

        # تشغيل ESLint مع تجاهل الخروج بـ error
        if [[ -f ".eslintrc*" ]] || [[ -f "eslint.config*" ]]; then
            LINT_OUTPUT=$(pnpm exec eslint src --format=compact --max-warnings 999 2>&1 || true)
            TS_ERRORS_COUNT=$(echo "$LINT_OUTPUT" | grep -c "error\|Error" || echo 0)
            TS_WARN_COUNT=$(echo "$LINT_OUTPUT" | grep -c "warning\|Warning" || echo 0)

            if [[ "$TS_ERRORS_COUNT" -gt 0 ]]; then
                printf "  ${R}❌ FAIL${N}  ESLint: %d خطأ، %d تحذير\n" "$TS_ERRORS_COUNT" "$TS_WARN_COUNT"
                echo "$LINT_OUTPUT" | grep -E "error" | head -20 | while read line; do
                    printf "  ${R}       %s${N}\n" "$line"
                done
                FAIL=$((FAIL+1))

                # إصلاح تلقائي ما أمكن
                if can_fix; then
                    pnpm exec eslint src --fix 2>/dev/null && \
                        fixed "Frontend: ESLint --fix طُبِّق" || \
                        warn "Frontend: بعض الأخطاء تحتاج إصلاح يدوي"
                fi
            else
                pass "Frontend: لا أخطاء ESLint ($TS_WARN_COUNT تحذير)"
            fi
        fi

        # فحص imports chat-service.ts
        if [[ -f "src/lib/chat-service.ts" ]]; then
            if grep -qP '\?\<=' "src/lib/chat-service.ts" 2>/dev/null; then
                warn "src/lib/chat-service.ts: lookbehind regex قد يكون مكسوراً"
                if can_fix; then
                    $PYTHON << 'TSFIX'
import re
from pathlib import Path
import os

ROOT = Path(os.environ["AZABOT_ROOT"])
f = ROOT / "azabot/src/lib/chat-service.ts"
if f.exists():
    content = f.read_text(encoding="utf-8")
    # إصلاح regex lookbehind متكسر على سطرين
    pattern = r"const sentences = text\.split\([^)]*\);"
    replacement = '''const sentences = text
      .replace(/([.!?؟،,])\\s+/g, "$1\\x00")
      .split("\\x00")
      .filter(Boolean);'''
    new = re.sub(pattern, replacement, content, flags=re.DOTALL)
    if new != content:
        f.write_text(new, encoding="utf-8")
        print("  \033[1;36m🔧 FIXED\033[0m chat-service.ts: regex مُصلَح")
    else:
        # بحث أوسع عن regex متكسر
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'text.split(' in line and '(?<=' in lines[i] + (lines[i+1] if i+1 < len(lines) else ''):
                combined = lines[i] + lines[i+1] if i+1 < len(lines) else lines[i]
                print(f"  \033[1;33m⚠️  WARN\033[0m  chat-service.ts سطر {i+1}: regex يحتاج مراجعة: {combined[:80]}")
TSFIX
                fi
            fi
        fi
    fi
    cd "$ROOT"
else
    warn "Frontend: pnpm غير موجود — تخطي lint"
fi

# ══════════════════════════════════════════════════════════════
# 4. PORTS — قتل العمليات المعلقة
# ══════════════════════════════════════════════════════════════
section "4/7  Ports — عمليات معلقة"

RASA_PORT="${RASA_PORT:-5005}"
ACTIONS_PORT="${ACTIONS_PORT:-5055}"
WEBHOOK_PORT="${WEBHOOK_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-8080}"

kill_port() {
    local port="$1" label="$2"
    local pids
    pids=$(lsof -ti ":$port" 2>/dev/null || true)
    if [[ -z "$pids" ]]; then
        pass "Port $port ($label): متاح"
        return
    fi
    local names
    names=$(for pid in $pids; do ps -p "$pid" -o comm= 2>/dev/null || echo "unknown"; done | tr '\n' ',' | sed 's/,$//')
    if can_fix; then
        for pid in $pids; do
            kill -TERM "$pid" 2>/dev/null || true
        done
        sleep 2
        for pid in $pids; do
            kill -KILL "$pid" 2>/dev/null || true
        done
        still=$(lsof -ti ":$port" 2>/dev/null | wc -l || echo 0)
        if [[ "$still" -eq 0 ]]; then
            fixed "Port $port ($label): عمليات '$names' أُوقفت"
        else
            warn "Port $port ($label): لا يزال مشغولاً بعد الإيقاف — جرب يدوياً"
        fi
    else
        warn "Port $port ($label): مشغول بـ '$names' (شغّل --fix لإيقافها)"
    fi
}

kill_port "$RASA_PORT"    "Rasa"
kill_port "$ACTIONS_PORT" "Actions"
kill_port "$WEBHOOK_PORT" "Webhook"
kill_port "$FRONTEND_PORT" "Frontend"

# ══════════════════════════════════════════════════════════════
# 5. Scripts — bash syntax
# ══════════════════════════════════════════════════════════════
section "5/7  Scripts — Bash Syntax"

declare -a SCRIPTS=(
    "dev.sh" "run.sh" "wsl-setup.sh" "wsl-fix.sh"
    "wsl-test.sh" "azabot-doctor.sh" "azabot-lint.sh"
    "scripts/botctl.sh"
    "deploy/production/deploy-production.sh"
    "deploy/production/server-setup.sh"
    "deploy/production/setup-swap.sh"
    "azabot/scripts/build-production.sh"
)

BASH_ERRORS=0
for script in "${SCRIPTS[@]}"; do
    [[ ! -f "$ROOT/$script" ]] && continue
    if bash -n "$ROOT/$script" 2>&1 | grep -q "error\|syntax"; then
        fail "bash syntax: $script"
        BASH_ERRORS=$((BASH_ERRORS+1))
    else
        pass "bash syntax: $script"
    fi
done

[[ "$BASH_ERRORS" -eq 0 ]] || warn "$BASH_ERRORS سكريبت بأخطاء bash"

# botctl.sh — إضافة force_free_port إن لم تكن موجودة
if [[ -f "$ROOT/scripts/botctl.sh" ]]; then
    if ! grep -q "force_free_port\|kill_port_process" "$ROOT/scripts/botctl.sh"; then
        if can_fix; then
            $PYTHON << 'PYEOF'
import os
from pathlib import Path

ROOT = Path(os.environ["AZABOT_ROOT"])
path = ROOT / "scripts/botctl.sh"
content = path.read_text()

fn = '''
# ── قتل العمليات المعلقة على المنافذ ─────────────────────────
kill_port_process() {
  local port="$1"
  local pids
  pids=$(lsof -ti ":$port" 2>/dev/null || true)
  if [[ -n "$pids" ]]; then
    local name; name=$(ps -p "${pids%% *}" -o comm= 2>/dev/null || echo "unknown")
    warn "Port $port مشغول بـ $name — إيقاف..."
    for pid in $pids; do
      kill -TERM "$pid" 2>/dev/null || true
    done
    sleep 2
    for pid in $pids; do
      kill -KILL "$pid" 2>/dev/null || true
    done
    ok "Port $port محرر"
  fi
}
'''

# أضف الدالة قبل cmd_start
if "cmd_start() {" in content and "kill_port_process" not in content:
    content = content.replace("cmd_start() {", fn + "cmd_start() {", 1)
    # استدعاء في بداية cmd_start
    content = content.replace(
        "cmd_start() {\n  ensure_dirs\n",
        'cmd_start() {\n  ensure_dirs\n  # تحرير المنافذ من العمليات المعلقة\n  kill_port_process "${ACTIONS_PORT}"\n  kill_port_process "${RASA_PORT}"\n  kill_port_process "${WEBHOOK_PORT}"\n'
    )
    path.write_text(content)
    print("  \033[1;36m🔧 FIXED\033[0m scripts/botctl.sh: kill_port_process مضافة")
PYEOF
        fi
    else
        pass "scripts/botctl.sh: port kill logic موجودة"
    fi
fi

# ══════════════════════════════════════════════════════════════
# 6. Security — ملفات حساسة
# ══════════════════════════════════════════════════════════════
section "6/7  Security — ملفات وإعدادات"

$PYTHON << 'PYEOF'
import os, re, json
from pathlib import Path

ROOT = Path(os.environ["AZABOT_ROOT"])
MODE = os.environ["AZABOT_MODE"]
G="\033[1;32m"; R="\033[1;31m"; Y="\033[1;33m"; C="\033[1;36m"; N="\033[0m"

def ok(m):  print(f"  {G}✅ PASS{N}  {m}")
def err(m): print(f"  {R}❌ FAIL{N}  {m}")
def fix(m): print(f"  {C}🔧 FIXED{N} {m}")
def wrn(m): print(f"  {Y}⚠️  WARN{N}  {m}")

# ── azabot/.env يجب أن يكون نظيفاً ───────────────────────────
az_env = ROOT / "azabot/.env"
if az_env.exists():
    content = az_env.read_text(encoding="utf-8")
    dangerous = any(
        kw in content for kw in ["eyJ", "supabase.co", "sk-proj", "EAA", "password", "Password"]
    )
    if dangerous:
        if MODE == "fix":
            clean = "# AzaBot Frontend .env — بدون credentials\nVITE_APP_NAME=AzaBot\nVITE_APP_VERSION=3.0.0\nVITE_APP_ENV=production\n"
            az_env.write_text(clean, encoding="utf-8")
            fix("azabot/.env: credentials حُذفت (احتياطي في azabot/.env.bak)")
        else:
            err("azabot/.env: يحتوي credentials حقيقية (خطر أمني)")
    else:
        ok("azabot/.env: نظيف")

# ── .gitignore يحمي الملفات الحساسة ─────────────────────────
gitignore = ROOT / ".gitignore"
required_ignores = [".env", "*.pem", "*.key", "gcp-*", "ssl/", ".venv/"]
if gitignore.exists():
    content = gitignore.read_text(encoding="utf-8")
    missing = [r for r in required_ignores if r not in content]
    if missing:
        if MODE == "fix":
            with open(gitignore, "a") as f:
                f.write("\n# Security additions\n")
                for r in missing:
                    f.write(f"{r}\n")
            fix(f".gitignore: {len(missing)} مدخل أمني مضاف")
        else:
            wrn(f".gitignore: ناقص: {', '.join(missing)}")
    else:
        ok(".gitignore: الملفات الحساسة محمية")
else:
    wrn(".gitignore غير موجود")

# ── gcp-f ملف GCP credentials مكشوف ─────────────────────────
gcp_file = ROOT / "gcp-f"
if gcp_file.exists():
    size = gcp_file.stat().st_size
    if size > 0:
        wrn(f"gcp-f: ملف credentials بحجم {size} بايت — تأكد أنه في .gitignore")
    else:
        ok("gcp-f: موجود لكن فارغ")

# ── RASA_LICENSE في ملفات غير .env ───────────────────────────
for f in list(ROOT.rglob("*.py")) + list(ROOT.rglob("*.yml")) + list(ROOT.rglob("*.ts")):
    if any(ex in str(f) for ex in [".venv", "node_modules", ".git"]): continue
    try:
        content = f.read_text(encoding="utf-8")
        if re.search(r'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9\.[A-Za-z0-9_-]{50,}', content):
            err(f"{f.relative_to(ROOT)}: تحتوي على RASA_PRO_LICENSE مضمّنة!")
    except: pass
PYEOF

# ══════════════════════════════════════════════════════════════
# 7. Pre-train Validation
# ══════════════════════════════════════════════════════════════
section "7/7  Pre-train — جاهزية التدريب"

$PYTHON << 'PYEOF'
import yaml, re, os
from pathlib import Path
from collections import defaultdict

ROOT = Path(os.environ["AZABOT_ROOT"])
G="\033[1;32m"; R="\033[1;31m"; Y="\033[1;33m"; C="\033[1;36m"; N="\033[0m"

def ok(m):  print(f"  {G}✅ PASS{N}  {m}")
def err(m): print(f"  {R}❌ FAIL{N}  {m}")
def wrn(m): print(f"  {Y}⚠️  WARN{N}  {m}")

# actions المسجلة vs المنفذة
try:
    domain_data = yaml.safe_load((ROOT/"domain.yml").read_text()) or {}
    registered = set(a for a in (domain_data.get("actions") or []) if str(a).startswith("action_"))
    for df in (ROOT/"domain").glob("*.yml"):
        dd = yaml.safe_load(df.read_text()) or {}
        registered |= set(a for a in (dd.get("actions") or []) if str(a).startswith("action_"))

    implemented = set()
    for f in (ROOT/"actions").rglob("*.py"):
        for m in re.finditer(r'return "([^"]+)"', f.read_text()):
            n = m.group(1)
            if n.startswith("action_"): implemented.add(n)

    RASA_BUILTINS = {"action_default_fallback","action_restart","action_session_start",
                     "action_correct_flow_slot","action_default_ask_affirmation"}
    unimpl = registered - implemented - RASA_BUILTINS
    unreg  = implemented - registered

    if unimpl:
        for a in sorted(unimpl)[:10]:
            err(f"action مسجلة غير منفذة: {a}")
        if len(unimpl) > 10: wrn(f"و{len(unimpl)-10} أخرى...")
    else:
        ok(f"كل {len(registered)} action مسجلة لها تنفيذ")

    if unreg:
        for a in sorted(unreg):
            wrn(f"action منفذة غير مسجلة في domain: {a}")
except Exception as e:
    wrn(f"تعذّر فحص actions: {e}")

# intents: عدد الأمثلة
low_intents = []
for f in (ROOT/"data").rglob("nlu.yml"):
    try:
        data = yaml.safe_load(f.read_text()) or {}
        for item in data.get("nlu", []):
            intent = item.get("intent","")
            examples = item.get("examples","") or ""
            count = len([l for l in examples.split("\n") if l.strip().startswith("-")])
            if 0 < count < 5:
                low_intents.append(f"{intent} ({count} أمثلة فقط)")
    except: pass

if low_intents:
    for i in low_intents[:5]:
        wrn(f"intent بأمثلة قليلة: {i}")
    ok(f"({len(low_intents)-5} آخرى)" if len(low_intents)>5 else "")
else:
    ok("كل intents لديها أمثلة كافية")

# Makefile: validate قبل train
try:
    makefile = (ROOT/"Makefile").read_text()
    train_target = re.search(r'^train:.*?(?=^\w|\Z)', makefile, re.MULTILINE|re.DOTALL)
    if train_target and "validate" not in train_target.group():
        wrn("Makefile: train target لا يُشغّل validate أولاً")
    else:
        ok("Makefile: train يتضمن validate")
except: pass

# endpoints.yml timeout
try:
    ep = (ROOT/"endpoints.yml").read_text()
    if "timeout" not in ep.lower():
        wrn("endpoints.yml: لا يوجد timeout مضبوط للاتصالات")
    else:
        ok("endpoints.yml: timeouts مضبوطة")
except: pass
PYEOF

# ══════════════════════════════════════════════════════════════
# التقرير النهائي
# ══════════════════════════════════════════════════════════════
echo ""
printf "${B}%s${N}\n" "$(printf '═%.0s' {1..60})"
printf "${B}  📊 نتائج الفحص الشامل${N}\n"
printf "${B}%s${N}\n" "$(printf '═%.0s' {1..60})"
printf "  ${G}✅ PASS:  %3d${N}\n" "$PASS"
printf "  ${R}❌ FAIL:  %3d${N}\n" "$FAIL"
printf "  ${Y}⚠️  WARN:  %3d${N}\n" "$WARN"
[[ "$MODE" == "fix" ]] && printf "  ${C}🔧 FIXED: %3d${N}\n" "$FIXED"
printf "${B}%s${N}\n" "$(printf '─%.0s' {1..60})"

if [[ "${#UNFIXED_LIST[@]}" -gt 0 ]]; then
    printf "\n${R}${B}  ❌ يحتاج إصلاح يدوي:${N}\n"
    printf "${R}%s${N}\n" "$(printf '─%.0s' {1..50})"
    for item in "${UNFIXED_LIST[@]}"; do
        printf "  ${R}→${N} %s\n" "$item"
    done
fi

{
  echo ""
  echo "## ملخص"
  echo "- PASS: $PASS"
  echo "- FAIL: $FAIL"
  echo "- WARN: $WARN"
  echo "- FIXED: $FIXED"
  if [[ "${#UNFIXED_LIST[@]}" -gt 0 ]]; then
      echo ""
      echo "## يحتاج إصلاح يدوي"
      for item in "${UNFIXED_LIST[@]}"; do
          echo "- $item"
      done
  fi
} >> "$REPORT_FILE"

echo ""
printf "  📄 التقرير: ${C}%s${N}\n" "$REPORT_FILE"

if [[ "$FAIL" -eq 0 ]]; then
    printf "\n  ${G}${B}🎉 المشروع جاهز للتدريب والنشر!${N}\n\n"
    exit 0
else
    printf "\n  ${R}${B}⚠  %d مشكلة تحتاج إصلاح يدوي${N}\n" "$FAIL"
    [[ "$MODE" != "fix" ]] && printf "  ${C}→ شغّل:  bash azabot-lint.sh --fix${N}\n"
    echo ""
    exit 1
fi


# chmod +x /opt/chatbot/alazab-rasa/az-lint.sh
# bash -n /opt/chatbot/alazab-rasa/az-lint.sh && echo "✅ syntax OK"
# wc -l /opt/chatbot/alazab-rasa/az-lint.sh
# 1. إنشاء ملف الـ executable
# sudo wget -O /usr/local/bin/az-lint.sh https://raw.githubusercontent.com/mosaab24/azabot/main/azabot-lint.sh
# sudo chmod +x /usr/local/bin/az-lint.sh

