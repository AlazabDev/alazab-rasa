#!/usr/bin/env bash
set -u

ENV_FILE="${1:-.env}"

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
NC="\033[0m"

ok()   { printf "${GREEN}[ok]${NC}    %s\n" "$*"; }
warn() { printf "${YELLOW}[warn]${NC}  %s\n" "$*"; }
fail() { printf "${RED}[fail]${NC}  %s\n" "$*"; }
info() { printf "${BLUE}[info]${NC}  %s\n" "$*"; }

[[ -f "$ENV_FILE" ]] || { fail "ملف $ENV_FILE غير موجود"; exit 1; }

echo -e "\n${BLUE}══ AzaBot — ENV Full Test ══${NC}\n"

# تحميل .env بدون تنفيذ أوامر
while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
  line="${raw_line%$'\r'}"

  [[ -z "$line" ]] && continue
  [[ "$line" =~ ^[[:space:]]*# ]] && continue
  [[ "$line" != *=* ]] && continue

  key="${line%%=*}"
  value="${line#*=}"

  key="$(echo "$key" | xargs)"

  # إزالة quotes بسيطة
  value="${value%\"}"
  value="${value#\"}"
  value="${value%\'}"
  value="${value#\'}"

  [[ -z "$key" ]] && continue
  export "$key=$value"
done < "$ENV_FILE"

required_vars=(
  NODE_ENV
  GEMINI_API_KEY
  CARTESIA_API_KEY
  ANTHROPIC_API_KEY
  ROBOFLOW_API_KEY
  ROBOFLOW_API_URL
  ROBOFLOW_PUBLIC_API_KEY
  LEMONSLICE_API_KEY
)

placeholder_regex='your_.*_here|placeholder|dummy|changeme|example|xxxxxx|xxxxx|todo|ضع_'

echo "── فحص وجود القيم ─────────────────────────"

missing=0
bad=0

for var in "${required_vars[@]}"; do
  value="${!var:-}"

  if [[ -z "$value" ]]; then
    warn "$var غير موجود أو فارغ"
    missing=$((missing + 1))
    continue
  fi

  if echo "$value" | grep -Eiq "$placeholder_regex"; then
    fail "$var يحتوي قيمة وهمية / placeholder"
    bad=$((bad + 1))
    continue
  fi

  len="${#value}"
  first="${value:0:4}"
  last="${value: -4}"

  if (( len <= 8 )); then
    warn "$var موجود لكن قصير جدًا length=$len"
  else
    ok "$var موجود length=$len masked=${first}****${last}"
  fi
done

echo
echo "── فحص روابط API ─────────────────────────"

if [[ -n "${ROBOFLOW_API_URL:-}" ]]; then
  case "$ROBOFLOW_API_URL" in
    https://api.roboflow.com|https://detect.roboflow.com)
      ok "ROBOFLOW_API_URL صحيح: $ROBOFLOW_API_URL"
      ;;
    https://app.roboflow.com/*)
      fail "ROBOFLOW_API_URL خطأ: هذا رابط لوحة تحكم وليس API endpoint"
      bad=$((bad + 1))
      ;;
    http://*)
      warn "ROBOFLOW_API_URL يستخدم http وليس https: $ROBOFLOW_API_URL"
      ;;
    https://*)
      warn "ROBOFLOW_API_URL غير قياسي، تأكد من الكود: $ROBOFLOW_API_URL"
      ;;
    *)
      fail "ROBOFLOW_API_URL ليس رابطًا صحيحًا: $ROBOFLOW_API_URL"
      bad=$((bad + 1))
      ;;
  esac
fi

echo
echo "── فحص NODE_ENV ─────────────────────────"

case "${NODE_ENV:-}" in
  production)
    warn "NODE_ENV=production — التدريب يجب أن يظل محظورًا إلا مع --force"
    ;;
  dev|development|test|local)
    ok "NODE_ENV=${NODE_ENV}"
    ;;
  "")
    warn "NODE_ENV غير محدد"
    ;;
  *)
    warn "NODE_ENV=${NODE_ENV} قيمة غير قياسية"
    ;;
esac

echo
echo "── اختبار اتصال APIs المتاحة ─────────────────────────"

http_test() {
  name="$1"
  url="$2"
  shift 2

  tmp="$(mktemp)"
  code="$(curl -sS -m 20 -o "$tmp" -w "%{http_code}" "$@" "$url" 2>/dev/null || true)"

  if [[ "$code" =~ ^2 ]]; then
    ok "$name اتصال ناجح HTTP $code"
  elif [[ "$code" == "401" || "$code" == "403" ]]; then
    fail "$name رفض المفتاح HTTP $code"
    bad=$((bad + 1))
  elif [[ "$code" == "000" || -z "$code" ]]; then
    warn "$name فشل اتصال/Timeout"
  else
    warn "$name رجع HTTP $code — راجع الرد المختصر:"
    head -c 300 "$tmp" | sed 's/[[:cntrl:]]/ /g'
    echo
  fi

  rm -f "$tmp"
}

if [[ -n "${GEMINI_API_KEY:-}" ]] && ! echo "$GEMINI_API_KEY" | grep -Eiq "$placeholder_regex"; then
  http_test "Gemini" "https://generativelanguage.googleapis.com/v1beta/models?key=${GEMINI_API_KEY}"
else
  warn "Gemini skipped"
fi

if [[ -n "${ANTHROPIC_API_KEY:-}" ]] && ! echo "$ANTHROPIC_API_KEY" | grep -Eiq "$placeholder_regex"; then
  http_test "Anthropic" "https://api.anthropic.com/v1/models" \
    -H "x-api-key: ${ANTHROPIC_API_KEY}" \
    -H "anthropic-version: 2023-06-01"
else
  warn "Anthropic skipped"
fi

if [[ -n "${ROBOFLOW_API_KEY:-}" ]] && [[ -n "${ROBOFLOW_API_URL:-}" ]] && ! echo "$ROBOFLOW_API_KEY" | grep -Eiq "$placeholder_regex"; then
  if [[ "$ROBOFLOW_API_URL" == "https://api.roboflow.com" ]]; then
    http_test "Roboflow" "${ROBOFLOW_API_URL}/?api_key=${ROBOFLOW_API_KEY}"
  else
    warn "Roboflow network test skipped لأن ROBOFLOW_API_URL ليس https://api.roboflow.com"
  fi
else
  warn "Roboflow skipped"
fi

echo
echo "── فحص Git Safety ─────────────────────────"

if [[ -f .gitignore ]]; then
  if grep -qx '\.env' .gitignore; then
    ok ".env موجود في .gitignore"
  else
    warn ".env غير موجود صراحة في .gitignore"
  fi
else
  warn ".gitignore غير موجود"
fi

if git ls-files --error-unmatch .env >/dev/null 2>&1; then
  fail ".env متتبع داخل Git — خطر، لازم git rm --cached .env"
  bad=$((bad + 1))
else
  ok ".env غير متتبع داخل Git"
fi

echo
echo "── النتيجة ─────────────────────────"

if (( bad > 0 )); then
  fail "فشل الاختبار: $bad مشكلة حرجة"
  exit 1
fi

if (( missing > 0 )); then
  warn "الاختبار اكتمل مع $missing متغير ناقص/فارغ"
  exit 2
fi

ok "كل فحوصات .env الأساسية نجحت"
