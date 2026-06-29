#!/usr/bin/env bash
# يُزيل الملفات الحساسة من تتبع git دون حذفها من القرص
# الاستخدام: bash scripts/git-untrack-secrets.sh && git commit -m "chore: untrack secrets"
set -euo pipefail
RED=$'\033[0;31m'; GREEN=$'\033[0;32m'; NC=$'\033[0m'

git rev-parse --git-dir &>/dev/null || { echo "ليس git repo"; exit 1; }

untrack() {
  if git ls-files --error-unmatch "$1" &>/dev/null 2>&1; then
    git rm --cached -r --force "$1" 2>/dev/null
    echo -e "  ${RED}✂️  untracked${NC}: $1"
  fi
}

for f in ".env" "azabot/.env" "ssl/" "RASA_LICENSE1" "RASA_LICENSE2" "RASA_LICENSE3" \
         ".runtime/" "scratch/" "webhook/static/uploads/"; do
  untrack "$f"
done

for f in $(git ls-files | grep -E '\.pem$|\.key$|\.crt$' 2>/dev/null || true); do
  untrack "$f"
done

echo -e "${GREEN}انتهى — راجع git status ثم commit${NC}"
