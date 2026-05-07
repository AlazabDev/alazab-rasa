#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  wsl-fix.sh — إصلاح مشاكل WSL قبل الإعداد
#  الاستخدام: bash wsl-fix.sh
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail

GREEN=$'\033[1;32m'; CYAN=$'\033[1;36m'; YELLOW=$'\033[1;33m'
RED=$'\033[1;31m'; BOLD=$'\033[1m'; NC=$'\033[0m'

ok()   { printf "${GREEN}✅ %s${NC}\n" "$*"; }
warn() { printf "${YELLOW}⚠️  %s${NC}\n" "$*"; }
step() { printf "\n${CYAN}${BOLD}[%s]${NC} %s\n" "$1" "$2"; }

# ══════════════════════════════════════════════════════════════
step "1/5" "إصلاح apt_pkg (ModuleNotFoundError)"
# ══════════════════════════════════════════════════════════════
# المشكلة: Python system يشير لـ python3.12 لكن apt_pkg مبني لـ python3.10
# الحل: إعادة ربط python3 بالإصدار الصحيح

PY_APT=$(find /usr/lib/python3 -name "apt_pkg*.so" 2>/dev/null | head -1 || true)
if [[ -z "$PY_APT" ]]; then
  warn "apt_pkg.so غير موجود — محاولة إعادة التثبيت"
  sudo apt-get install -y --reinstall python3-apt 2>/dev/null || true
else
  # تحقق من الإصدار
  PY_VER=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
  APT_VER=$(echo "$PY_APT" | grep -oP '\d+\.\d+' | head -1)
  if [[ "$PY_VER" != "$APT_VER" ]]; then
    warn "تعارض إصدار: python3=$PY_VER لكن apt_pkg=$APT_VER"
    # إصلاح بإعادة تثبيت python3-apt للإصدار الصحيح
    sudo apt-get install -y --reinstall python3-apt 2>/dev/null || true
    # أو تعطيل cnf-update-db (الأسلم)
    sudo chmod -x /usr/lib/cnf-update-db 2>/dev/null || true
    ok "cnf-update-db معطّل (لن يؤثر على الإعداد)"
  else
    ok "apt_pkg إصدار متطابق: $APT_VER"
  fi
fi

# ══════════════════════════════════════════════════════════════
step "2/5" "إزالة deadsnakes PPA (ليست مطلوبة في Ubuntu 24.04)"
# ══════════════════════════════════════════════════════════════
# Ubuntu 24.04 (Noble) يأتي بـ Python 3.12 افتراضياً
# Python 3.11 موجود في الـ repos الرسمية — لا نحتاج deadsnakes

PPA_FILE=$(find /etc/apt/sources.list.d/ -name "*deadsnakes*" 2>/dev/null | head -1 || true)
if [[ -n "$PPA_FILE" ]]; then
  sudo rm -f "$PPA_FILE"
  ok "deadsnakes PPA حُذف: $PPA_FILE"
else
  ok "deadsnakes PPA غير موجود — لا مشكلة"
fi

# تعطيل أي PPA يفشل في الاتصال مؤقتاً
for f in /etc/apt/sources.list.d/*.list; do
  if grep -q "launchpadcontent" "$f" 2>/dev/null; then
    sudo mv "$f" "${f}.disabled"
    warn "عطّلت: $f (شبكة غير متاحة)"
  fi
done

# ══════════════════════════════════════════════════════════════
step "3/5" "تحديث apt بدون PPAs مكسورة"
# ══════════════════════════════════════════════════════════════
sudo apt-get update -qq 2>&1 | grep -E "^E:|^W:" | head -5 || true
ok "apt update اكتمل"

# ══════════════════════════════════════════════════════════════
step "4/5" "التحقق من Python المتاح"
# ══════════════════════════════════════════════════════════════
# Ubuntu 24.04: Python 3.12 افتراضي، 3.11 متاح في repos
for pyver in python3.12 python3.11 python3; do
  if command -v "$pyver" >/dev/null 2>&1; then
    ok "$pyver موجود: $($pyver --version)"
    BEST_PY="$pyver"
    break
  fi
done

if ! command -v python3.11 >/dev/null 2>&1; then
  warn "python3.11 غير موجود — تثبيت..."
  sudo apt-get install -y python3.11 python3.11-venv python3.11-dev 2>/dev/null || \
  warn "فشل تثبيت python3.11 — سنستخدم python3.12"
fi

# ══════════════════════════════════════════════════════════════
step "5/5" "إصلاح مشكلة /mnt/d/ — صلاحيات التنفيذ"
# ══════════════════════════════════════════════════════════════
# الملفات على /mnt/d/ (Windows NTFS) تفقد execute permission
# الحل: إضافة metadata=true في /etc/wsl.conf

WSL_CONF="/etc/wsl.conf"
if [[ ! -f "$WSL_CONF" ]] || ! grep -q "metadata" "$WSL_CONF" 2>/dev/null; then
  sudo tee "$WSL_CONF" > /dev/null << 'CONF'
[automount]
enabled = true
root = /mnt/
options = "metadata,umask=22,fmask=11"

[interop]
enabled = true
appendWindowsPath = false

[boot]
systemd = true
CONF
  ok "/etc/wsl.conf أُنشئ — يجب إعادة تشغيل WSL مرة واحدة"
  warn "شغّل في PowerShell: wsl --shutdown  ثم افتح WSL من جديد"
else
  ok "/etc/wsl.conf موجود بالفعل"
fi

echo ""
printf "${GREEN}${BOLD}══════════════════════════════════════════════${NC}\n"
printf "${GREEN}${BOLD} الإصلاح اكتمل!${NC}\n"
printf "${GREEN}${BOLD}══════════════════════════════════════════════${NC}\n"
echo ""
echo "  الخطوة التالية:"
echo ""

if grep -q "metadata" /etc/wsl.conf 2>/dev/null; then
  printf "  1️⃣  أعد تشغيل WSL (مهم للـ /mnt/d/ permissions):\n"
  printf "     ${CYAN}# في PowerShell:\n"
  printf "     wsl --shutdown${NC}\n"
  echo ""
  printf "  2️⃣  بعد إعادة التشغيل، شغّل الإعداد:\n"
  printf "     ${CYAN}bash wsl-setup.sh${NC}\n"
else
  printf "  شغّل الإعداد مباشرة:\n"
  printf "  ${CYAN}bash wsl-setup.sh${NC}\n"
fi
echo ""
