#!/bin/bash

# pre_train_check.sh - فحص شامل قبل التدريب لضمان نجاحه
# ========================================================
# هذا السكربت يقوم بفحص البيانات، الاتصالات، والترخيص قبل بدء التدريب.

set -e

echo "🔍 بدء الفحص الشامل قبل التدريب..."

# 1. التحقق من البيانات (rasa data validate)
echo -n "✓ التحقق من صيغة البيانات (YAML و Intents)... "
if rasa data validate >/dev/null 2>&1; then
    echo "✅"
else
    echo "❌"
    echo "⚠️  فشل التحقق من البيانات. قم بتشغيل 'rasa data validate' لرؤية التفاصيل."
    exit 1
fi

# 2. التحقق من الـ Actions
echo -n "✓ التحقق من كود الـ Actions... "
if python -c "import actions" >/dev/null 2>&1; then
    echo "✅"
else
    echo "❌"
    echo "⚠️  يوجد خطأ برمجي (Syntax Error) في مجلد actions/."
    exit 1
fi

# 3. التحقق من Action Server
echo -n "✓ التحقق من Action Server (Port 5055)... "
if curl -s -f http://127.0.0.1:5055/health >/dev/null; then
    echo "✅"
else
    echo "⚠️  (تحذير) Action Server لا يستجيب. هذا لن يمنع التدريب لكنه سيمنع تشغيل البوت لاحقاً."
fi

# 4. التحقق من قاعدة البيانات
echo -n "✓ التحقق من اتصال قاعدة البيانات (PostgreSQL)... "
# تحميل متغيرات البيئة من .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

if [ -n "$SUPABASE_DB_PASSWORD" ] && [ -n "$DB_HOST" ]; then
    if PGPASSWORD=$SUPABASE_DB_PASSWORD psql -h $DB_HOST -U postgres -d postgres -c "SELECT 1" >/dev/null 2>&1; then
        echo "✅"
    else
        echo "⚠️  (تحذير) فشل الاتصال بقاعدة البيانات. تأكد من إعدادات SUPABASE."
    fi
else
    echo "⚠️  (تحذير) متغيرات قاعدة البيانات غير متوفرة في .env"
fi

# 5. التحقق من OpenAI API
echo -n "✓ التحقق من اتصال OpenAI API (CALM Model)... "
if [ -n "$OPENAI_API_KEY" ]; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY")
    if [ "$HTTP_CODE" == "200" ]; then
        echo "✅"
    else
        echo "❌"
        echo "⚠️  OpenAI API Key غير صحيح أو الخدمة متوقفة."
        exit 1
    fi
else
    echo "❌"
    echo "⚠️  OPENAI_API_KEY غير موجود في البيئة. هذا مطلوب لـ CALM."
    exit 1
fi

# 6. التحقق من الضوضاء في البيانات (اختياري)
echo "✓ جاري تنظيف الفراغات الزائدة في ملفات NLU..."
find data/nlu/ -name "*.yml" -exec sed -i 's/^[[:space:]]*$//' {} +
find data/nlu/ -name "*.yml" -exec sed -i 's/[[:space:]]*$//' {} +

echo "----------------------------------------------------"
echo "✅ جميع الفحوصات الحرجة اجتازت بنجاح! يمكنك الآن بدء التدريب."
echo "لتدريب البوت، شغل: make train"
echo "----------------------------------------------------"
