#!/usr/bin/env bash
# إضافة 4GB swap لضمان عدم انهيار الخادم عند تحميل Rasa
set -euo pipefail

SWAP_FILE="/swapfile"
SWAP_SIZE="4G"

if swapon --show | grep -q "$SWAP_FILE"; then
  echo "✅ Swap موجود بالفعل:"
  swapon --show
  exit 0
fi

echo "→ إنشاء $SWAP_SIZE swap..."
sudo fallocate -l $SWAP_SIZE $SWAP_FILE
sudo chmod 600 $SWAP_FILE
sudo mkswap $SWAP_FILE
sudo swapon $SWAP_FILE

# تفعيل عند إعادة التشغيل
echo "$SWAP_FILE none swap sw 0 0" | sudo tee -a /etc/fstab

# ضبط swappiness مناسب للخادم (منخفض = يستخدم الـ swap فقط عند الحاجة)
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
echo "vm.vfs_cache_pressure=50" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p >/dev/null

echo "✅ Swap $SWAP_SIZE مُضاف ومُفعَّل"
free -h
