#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  scripts/git-untrack-secrets.sh
#  يُزيل الملفات الحساسة من تتبع git دون حذفها من القرص
#
#  لماذا هذا الملف ضروري؟
#  ─────────────────────────────────────────────────────────────
#  .gitignore يمنع إضافة ملفات جديدة فقط.
#  إذا كانت الملفات مُتتبَّعة بالفعل في git (git ls-files تُظهرها)
#  فـ .gitignore لا يؤثر عليها — يجب استخدام git rm --cached
#
#  الاستخدام (مرة واحدة بعد clone):
#    bash scripts/git-untrack-secrets.sh
#    git commit -m "chore: untrack sensitive files"
# ══════════════════════════════════════════════════════════════
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
UNTRACKED=0; SKIPPED=0

untrack() {
  local path="$1"
  if git ls-files --error-unmatch "$path" &>/dev/null 2>&1; then
    git rm --cached -r --force "$path" 2>/dev/null
    echo -e "  ${RED}✂️  untracked${NC}: $path"
    ((UNTRACKED++))
  else
    echo -e "  ${GREEN}✓ already ignored${NC}: $path"
    ((SKIPPED++))
  fi
}

# تحقق أننا داخل git repo
git rev-parse --git-dir &>/dev/null || {
  echo -e "${RED}[fail]${NC} ليس git repo — شغّل 'git init' أولاً"
  exit 1
}

echo -e "\n${YELLOW}══ إزالة الملفات الحساسة من git tracking ══${NC}\n"

# ── أسرار البيئة ──────────────────────────────────────────────
untrack ".env"
untrack "azabot/.env"
# كل ملفات .env.* ما عدا .example
for f in $(git ls-files | grep '\.env' | grep -v '\.example' || true); do
  untrack "$f"
done

# ── شهادات SSL ────────────────────────────────────────────────
untrack "ssl/"
for f in $(git ls-files | grep -E '\.pem$|\.key$|\.crt$|\.p12$' || true); do
  untrack "$f"
done

# ── تراخيص Rasa ───────────────────────────────────────────────
for license in RASA_LICENSE1 RASA_LICENSE2 RASA_LICENSE3; do
  untrack "$license"
done

# ── بيانات Runtime ────────────────────────────────────────────
untrack ".runtime/sessions.json"
untrack ".runtime/admin-data.json"
untrack ".runtime/pids/"
# كل محتوى .runtime/
for f in $(git ls-files | grep '\.runtime/' || true); do
  untrack "$f"
done

# ── ملفات scratch ─────────────────────────────────────────────
untrack "scratch/"

# ── Google Credentials ────────────────────────────────────────
for f in $(git ls-files | grep -E 'gcp-.*\.json|service-account.*\.json|credentials\.json' || true); do
  untrack "$f"
done

# ── نماذج Rasa (حجم ضخم) ─────────────────────────────────────
for f in $(git ls-files | grep -E 'models/.*\.tar\.gz' || true); do
  untrack "$f"
done

# ── ملفات المستخدمين المرفوعة ─────────────────────────────────
untrack "webhook/static/uploads/"
for f in $(git ls-files | grep 'webhook/static/uploads/' || true); do
  untrack "$f"
done

# ── إعادة التحقق: هل لا تزال هناك ملفات حساسة مُتتبَّعة? ───
echo ""
echo -e "${YELLOW}══ فحص ما تبقى في git tracking ══${NC}"
REMAINING=$(git ls-files | grep -E \
  '\.env$|\.pem$|\.key$|\.crt$|RASA_LICENSE[123]|\.runtime/|/uploads/' \
  | grep -v '\.example' || true)

if [[ -n "$REMAINING" ]]; then
  echo -e "${RED}⚠️  لا تزال هذه الملفات مُتتبَّعة:${NC}"
  echo "$REMAINING" | while read -r f; do echo "  - $f"; done
else
  echo -e "${GREEN}✅ لا توجد ملفات حساسة مُتتبَّعة${NC}"
fi

# ── الخطوة التالية ────────────────────────────────────────────
echo ""
echo -e "${YELLOW}══ الخطوات التالية ══${NC}"
echo "  1. راجع التغييرات:  git status"
echo "  2. Commit التنظيف:  git commit -m 'chore: untrack sensitive files from git'"
echo "  3. إذا الملفات في تاريخ git القديم:"
echo "     git filter-repo --invert-paths --path .env --path ssl/ --force"
echo "     أو: BFG Repo Cleaner — https://rtyley.github.io/bfg-repo-cleaner/"
echo ""
echo -e "${GREEN}إجمالي: untracked=$UNTRACKED | already-clean=$SKIPPED${NC}"
