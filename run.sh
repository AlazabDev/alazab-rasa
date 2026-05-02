#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
#  run.sh — AzaBot Unified Launcher (بضغطة واحدة)
#
#  الاستخدام:
#    bash run.sh              → تشغيل الكل (باك + فرونت)
#    bash run.sh --backend    → باك فقط (actions + rasa + webhook)
#    bash run.sh --frontend   → فرونت فقط
#    bash run.sh --skip-train → تشغيل بدون تدريب جديد
#    bash run.sh stop         → إيقاف كل شيء
#    bash run.sh status       → حالة الخدمات
#    bash run.sh logs [svc]   → سجلات (all|actions|rasa|webhook|frontend)
# ══════════════════════════════════════════════════════════════
set -Eeuo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# تفويض مباشر لـ dev.sh
exec bash "$ROOT_DIR/dev.sh" "$@"
