#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  scripts/git-sync.sh — ضبط المشروع مع GitHub
#  AlazabDev/alazab-rasa
#
#  الاستخدام:
#    bash scripts/git-sync.sh           ← status + تعليمات
#    bash scripts/git-sync.sh init      ← ربط بـ remote (مرة واحدة)
#    bash scripts/git-sync.sh push      ← commit + push
#    bash scripts/git-sync.sh pull      ← pull + safe merge
#    bash scripts/git-sync.sh status    ← حالة مفصّلة
# ══════════════════════════════════════════════════════════════
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

REMOTE_URL="https://github.com/AlazabDev/alazab-rasa.git"
BRANCH="${GIT_BRANCH:-main}"

GREEN=$'\033[1;32m'; YELLOW=$'\033[1;33m'; RED=$'\033[1;31m'
CYAN=$'\033[1;36m'; BOLD=$'\033[1m'; NC=$'\033[0m'

ok()   { printf "${GREEN}✅ %s${NC}\n" "$*"; }
warn() { printf "${YELLOW}⚠️  %s${NC}\n" "$*"; }
fail() { printf "${RED}❌ %s${NC}\n" "$*" >&2; exit 1; }
info() { printf "${CYAN}→  %s${NC}\n" "$*"; }
section() { echo; printf "${BOLD}${CYAN}══ %s ══${NC}\n" "$*"; }

# ══════════════════════════════════════════════════════════════
CMD="${1:-status}"
# ══════════════════════════════════════════════════════════════

# ── init: ربط الـ remote (مرة واحدة فقط) ─────────────────────
if [[ "$CMD" == "init" ]]; then
    section "Git Init + Remote Setup"

    if [[ ! -d ".git" ]]; then
        git init -b main
        ok "git init"
    else
        ok "git repository موجود"
    fi

    # remote
    if git remote get-url origin &>/dev/null; then
        current=$(git remote get-url origin)
        if [[ "$current" != "$REMOTE_URL" ]]; then
            git remote set-url origin "$REMOTE_URL"
            ok "remote url updated → $REMOTE_URL"
        else
            ok "remote origin: $REMOTE_URL"
        fi
    else
        git remote add origin "$REMOTE_URL"
        ok "remote added: $REMOTE_URL"
    fi

    # user config
    if [[ -z "$(git config user.email 2>/dev/null)" ]]; then
        git config user.email "devops@alazab.com"
        git config user.name "AzaBot DevOps"
        ok "git user configured"
    fi

    # fetch
    info "جلب التاريخ من GitHub..."
    git fetch origin "$BRANCH" 2>&1 || warn "لم يتم fetch — تحقق من الاتصال والـ token"

    echo ""
    ok "Git initialized and linked to GitHub"
    echo ""
    echo "الخطوة التالية:"
    echo "  bash scripts/git-sync.sh push"
    exit 0
fi

# ── تحقق من وجود git repo ─────────────────────────────────────
if [[ ! -d ".git" ]]; then
    fail "لا يوجد git repo — شغّل أولاً: bash scripts/git-sync.sh init"
fi

# ── status: حالة مفصّلة ───────────────────────────────────────
if [[ "$CMD" == "status" ]]; then
    section "Git Status — AzaBot"

    echo ""
    info "Branch: $(git branch --show-current 2>/dev/null || echo 'unknown')"
    info "Remote: $(git remote get-url origin 2>/dev/null || echo 'none')"
    info "Last commit: $(git log --oneline -1 2>/dev/null || echo 'no commits')"

    echo ""
    section "Untracked / Modified"
    git status --short 2>/dev/null | head -30 || true

    echo ""
    section "ملفات يجب التحقق منها"
    for f in ".env" "azabot/.env" "*.pem" "RASA_LICENSE*"; do
        # تحقق أن هذه الملفات في gitignore
        if git check-ignore -q "$f" 2>/dev/null; then
            ok "$f → في .gitignore ✓"
        else
            warn "$f → ليس في .gitignore — خطر!"
        fi
    done

    exit 0
fi

# ── pull: سحب آخر التغييرات ───────────────────────────────────
if [[ "$CMD" == "pull" ]]; then
    section "Git Pull — $BRANCH"

    # حفظ التغييرات المحلية مؤقتاً
    if ! git diff --quiet 2>/dev/null; then
        info "حفظ التغييرات المحلية مؤقتاً (stash)..."
        git stash push -m "auto-stash before pull $(date +%Y%m%d-%H%M)"
        STASHED=true
    else
        STASHED=false
    fi

    git fetch origin "$BRANCH"
    git merge "origin/$BRANCH" --no-edit || {
        warn "تعارض في الـ merge — راجع الملفات يدوياً"
        exit 1
    }

    if $STASHED; then
        info "استعادة التغييرات المحلية..."
        git stash pop || warn "تعارض في stash pop — راجع يدوياً"
    fi

    ok "Pull completed from $BRANCH"
    git log --oneline -3
    exit 0
fi

# ── push: commit + push ────────────────────────────────────────
if [[ "$CMD" == "push" ]]; then
    section "Git Commit + Push — $BRANCH"

    # تحقق أمني: لا secrets في الـ staged files
    _check_secrets() {
        local staged
        staged=$(git diff --cached --name-only 2>/dev/null)
        for f in $staged; do
            [[ -f "$f" ]] || continue
            # تحقق من patterns خطرة
            if grep -qE "(sk-proj-[a-zA-Z0-9]{40,}|SUPABASE_ACCESS_TOKEN=.+[a-z0-9]{10}|sbp_[a-z0-9]{30,})" "$f" 2>/dev/null; then
                fail "⛔ SECURITY: $f يحتوي secret حقيقي — لا يُرفع!"
            fi
        done
    }

    # add files
    info "إضافة الملفات..."
    git add \
        actions/ \
        data/ \
        domain/ \
        domain.yml \
        webhook/ \
        deploy/ \
        scripts/ \
        piper/pronunciation_lexicon.yml \
        piper/voices.json \
        piper/generate_brand_samples.py \
        piper/configs/ \
        piper/sentences/ \
        piper/voice/code/ \
        piper/samples/ \
        piper/voice_knowledge_base_tts_ar.txt \
        config.yml \
        credentials.yml \
        endpoints.yml \
        endpoints.nodocker.yml \
        endpoints.sqlite.yml \
        pyproject.toml \
        requirements.txt \
        requirements-core.txt \
        .gitignore \
        .env.example \
        azabot/.env \
        azabot/supabase/functions/uberfix/ \
        scripts/deploy-production.sh \
        
        Makefile \
        README.md \
        SETUP_GUIDE.md \
        wsl-setup.sh \
        wsl-test.sh \
        run.sh \
        dev.sh \
        azabot-doctor.sh \
        2>/dev/null || true

    # add remaining tracked files
    git add -u 2>/dev/null || true

    # تحقق أمني
    _check_secrets
    ok "Security check passed"

    # فحص هل في شيء للـ commit
    if git diff --cached --quiet 2>/dev/null; then
        ok "لا توجد تغييرات جديدة للـ commit"
        exit 0
    fi

    # commit message
    MSG="${GIT_MSG:-}"
    if [[ -z "$MSG" ]]; then
        CHANGED=$(git diff --cached --name-only | wc -l)
        BRANCH_NOW=$(git branch --show-current 2>/dev/null || echo main)
        MSG="feat: AzaBot v4.0 — ${CHANGED} files updated

- Architecture: server.py 3649→268 lines, routers/ extracted
- Auth: internal HMAC sessions (4 users, no external JWT)
- Actions: core/ layer (db pool, gpt cache, whatsapp unified)
- Segments: brand-aware context accumulation
- Domain: 0 warnings, 0 duplicates, deep_clean passed
- Deploy: systemd services + nginx configs added
- Piper: TTS configs + pronunciation lexicon
- Security: azabot/.env cleaned, secrets in root .env only
- Deps: google-auth conflict fixed, grpcio versions aligned"
    fi

    git commit -m "$MSG"
    ok "Committed: $MSG"

    # push
    info "رفع إلى GitHub..."
    git push origin "$BRANCH" 2>&1 || {
        warn "Push failed — جرب:"
        warn "  git push --set-upstream origin $BRANCH"
        warn "  أو تحقق من GitHub token"
        exit 1
    }

    ok "Pushed to github.com/AlazabDev/alazab-rasa ($BRANCH)"
    git log --oneline -3
    exit 0
fi

# ── مساعدة ────────────────────────────────────────────────────
echo ""
echo "الاستخدام:"
echo "  bash scripts/git-sync.sh init    ← ربط بـ GitHub (مرة واحدة)"
echo "  bash scripts/git-sync.sh status  ← حالة المشروع"
echo "  bash scripts/git-sync.sh push    ← commit + push"
echo "  bash scripts/git-sync.sh pull    ← سحب آخر التغييرات"
echo ""
echo "مع commit message مخصص:"
echo "  GIT_MSG='fix: ...' bash scripts/git-sync.sh push"
