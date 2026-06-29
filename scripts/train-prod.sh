#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  scripts/train-prod.sh — حماية التدريب من بيئة الإنتاج
#  الاستخدام:
#    bash scripts/train-prod.sh             # تدريب (يُحظر في prod)
#    bash scripts/train-prod.sh --validate  # تحقق فقط، بدون تدريب
#    bash scripts/train-prod.sh --force     # تجاوز الحظر (خطر)
# ══════════════════════════════════════════════════════════════
set -euo pipefail

BLUE=$'\033[1;34m'; GREEN=$'\033[1;32m'; RED=$'\033[1;31m'; YELLOW=$'\033[1;33m'; NC=$'\033[0m'

FORCE=false; VALIDATE_ONLY=false
for arg in "$@"; do
  [[ "$arg" == "--force" ]] && FORCE=true
  [[ "$arg" == "--validate" ]] && VALIDATE_ONLY=true
done

log()  { printf "${BLUE}[train]${NC} %s\n" "$*"; }
ok()   { printf "${GREEN}[ok]${NC}    %s\n" "$*"; }
warn() { printf "${YELLOW}[warn]${NC}  %s\n" "$*"; }
fail() { printf "${RED}[fail]${NC}  %s\n" "$*" >&2; exit 1; }

echo -e "\n${BLUE}══ AzaBot — Rasa Training Guard ══${NC}\n"

# ── [إن وُجد .env] حمّله للتحقق من NODE_ENV ───────────────────
if [[ -f .env ]]; then
  set +u
  line=""; key=""; value=""
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" == \#* || "$line" != *=* ]] && continue
    key="${line%%=*}"; value="${line#*=}"
    key="$(echo "$key" | xargs)"
    value="${value%\"}"; value="${value#\"}"
    value="${value%\'}"; value="${value#\'}"
    export "$key=$value"
  done < .env
  set -u
fi

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

VENV_DIR="${VENV_DIR:-.venv}"

PYTHON_BIN="${PYTHON_BIN:-python3}"
if [[ -x "$VENV_DIR/bin/python" ]]; then
  PYTHON_BIN="$VENV_DIR/bin/python"
fi

RASA_BIN="${RASA_BIN:-rasa}"
if [[ -x "$VENV_DIR/bin/rasa" ]]; then
  RASA_BIN="$VENV_DIR/bin/rasa"
fi

DOMAIN_FILE="${DOMAIN_FILE:-.runtime/domain.generated.yml}"
ENDPOINTS_FILE="${ENDPOINTS_FILE:-.runtime/endpoints.generated.yml}"

# ══ ⛔ GUARD 1: حظر التدريب في بيئة الإنتاج ════════════════════
if [[ "${NODE_ENV:-}" == "production" ]]; then
  if [[ "$FORCE" == "true" ]]; then
    warn "بيئة إنتاج + --force: تجاوز الحظر بشكل صريح — هذا خطر"
  else
    echo ""
    echo -e "${RED}╔═══════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║  ⛔  التدريب محظور في بيئة الإنتاج                ║${NC}"
    echo -e "${RED}║                                                   ║${NC}"
    echo -e "${RED}║  NODE_ENV=production يعني أن السيرفر يخدم          ║${NC}"
    echo -e "${RED}║  مستخدمين حقيقيين الآن. التدريب سيستهلك RAM/CPU    ║${NC}"
    echo -e "${RED}║  ويُبطّئ البوت، والنموذج الجديد غير مُختبَر.       ║${NC}"
    echo -e "${RED}║                                                   ║${NC}"
    echo -e "${RED}║  الحل الصحيح:                                     ║${NC}"
    echo -e "${RED}║   1. NODE_ENV=dev bash scripts/train-prod.sh      ║${NC}"
    echo -e "${RED}║   2. rasa test  اختبر النموذج محلياً              ║${NC}"
    echo -e "${RED}║   3. scp models/*.tar.gz user@server:/opt/azabot/ ║${NC}"
    echo -e "${RED}║   4. sudo systemctl restart azabot-rasa           ║${NC}"
    echo -e "${RED}║                                                   ║${NC}"
    echo -e "${RED}║  للتجاوز القسري غير منصوح به: --force             ║${NC}"
    echo -e "${RED}╚═══════════════════════════════════════════════════╝${NC}"
    echo ""
    exit 1
  fi
fi

# ══ ⛔ GUARD 2: TRAIN_ON_DEPLOY=true محظور بدون --force ═══════
if [[ "${TRAIN_ON_DEPLOY:-false}" == "true" ]] && [[ "$FORCE" != "true" ]]; then
  fail "TRAIN_ON_DEPLOY=true محظور — اضبطه على false في .env الإنتاج"
fi

# ══ ✅ توليد ملفات Rasa النهائية من ملفات includes قبل التحقق/التدريب ══
log "توليد domain/endpoints runtime..."
"$PYTHON_BIN" scripts/render_runtime_domain.py >/dev/null

[[ -f "$DOMAIN_FILE" ]] || fail "ملف الدومين النهائي مفقود: $DOMAIN_FILE"
[[ -f "$ENDPOINTS_FILE" ]] || fail "ملف endpoints النهائي مفقود: $ENDPOINTS_FILE"

ok "runtime جاهز: $DOMAIN_FILE + $ENDPOINTS_FILE"

# ══ ✅ التحقق من صحة YAML قبل أي شيء ═══════════════════════════
log "التحقق من صحة ملفات YAML..."
"$PYTHON_BIN" - << 'PYEOF'
import sys, os
try:
    import yaml
except ImportError:
    print("  ⚠️  PyYAML غير متاح — تخطي")
    sys.exit(0)

errors, files = [], []

for root, dirs, fs in os.walk("."):
    dirs[:] = [
        d for d in dirs
        if d not in ("node_modules", ".venv", "venv", ".git", "__pycache__", "models")
    ]

    for f in fs:
        if f.endswith((".yml", ".yaml")):
            files.append(os.path.join(root, f))

for fpath in sorted(files):
    try:
        with open(fpath, encoding="utf-8") as fh:
            yaml.safe_load(fh)
    except yaml.YAMLError as e:
        errors.append(f"  ❌ {fpath}: {e}")

if errors:
    print(f"\n{len(errors)} ملف به أخطاء:")
    for e in errors:
        print(e)
    sys.exit(1)

print(f"  ✅ {len(files)} ملف YAML — جميعها صحيحة")
PYEOF

# ══ ✅ rasa data validate ═══════════════════════════════════════
log "rasa data validate..."
if [[ -x "$RASA_BIN" ]] || command -v "$RASA_BIN" &>/dev/null; then
  "$RASA_BIN" data validate \
    --domain "$DOMAIN_FILE" \
    --data data/ \
    --endpoints "$ENDPOINTS_FILE" \
    2>&1 | tail -40

  ok "rasa data validate — نجح"
else
  warn "rasa CLI غير متاح — تخطي"
fi

[[ "$VALIDATE_ONLY" == "true" ]] && { ok "وضع التحقق فقط — اكتمل"; exit 0; }

# ══ 🚀 التدريب ═══════════════════════════════════════════════
log "بدء التدريب..."
mkdir -p models
START=$(date +%s)

"$RASA_BIN" train \
  --domain "$DOMAIN_FILE" \
  --data data/ \
  --config config.yml \
  --out models/ \
  --fixed-model-name "alazab-$(date +%Y%m%d-%H%M)"

ELAPSED=$(( $(date +%s) - START ))
ok "التدريب اكتمل في $((ELAPSED/60))د $((ELAPSED%60))ث"

ls -lh models/*.tar.gz 2>/dev/null | tail -3

echo ""
echo -e "${GREEN}══ الخطوات التالية ══${NC}"
echo "  اختبار:    bash az.sh test"
echo "  تشغيل:     bash az.sh on"
echo "  حالة:      bash az.sh status"