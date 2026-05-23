# دليل التشغيل — السيرفر الفعلي
## AzaBot v4.0 على Ubuntu/WSL

---

## الوضع الحالي ✅

المشروع مكتمل برمجياً وجاهز للتدريب:
- **72 Python** — 0 errors
- **66+ YAML** — 0 errors, 0 duplicates
- **deep_clean** — ✅ passed
- **render_runtime_domain** — ✅ no warnings
- **Generated domain** — 83 intents · 52 actions · 117 responses

---

## ⚠️ حل مشكلة google-auth Conflict

إذا ظهر هذا الخطأ عند `bash scripts/botctl.sh setup`:
```
ERROR: Cannot install google-auth==2.41.1 because google-cloud-aiplatform needs >=2.47.0
```

**الحل:** ملف requirements.txt مُحدَّث يحل هذا الـ conflict تلقائياً.

**طريقة التثبيت الصحيحة:**

```bash
# الطريقة 1 — بـ pyproject.toml (الأفضل لـ Rasa)
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"

# الطريقة 2 — بـ requirements.txt المُصحَّح
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# الطريقة 3 — core فقط (للاختبار السريع)
pip install -r requirements-core.txt
```

**أو بأمر واحد ذكي:**
```bash
bash scripts/install-deps.sh
```

---

## خطوات التشغيل بالترتيب

### الخطوة 1 — إعداد البيئة (مرة واحدة)

```bash
cd ~/azabot/alazab-rasa

# إنشاء venv وتثبيت المتطلبات
bash scripts/botctl.sh setup
```

### الخطوة 2 — التحقق من .env

```bash
# تأكد من وجود المتغيرات التالية في .env
bash scripts/validate-backend-env.sh
```

المتغيرات الحيوية الموجودة فعلاً:
```
✅ RASA_PRO_LICENSE      — موجود
✅ OPENAI_API_KEY        — موجود
✅ ADMIN_PASSWORD        — موجود
✅ ADMIN_SESSION_SECRET  — موجود
✅ DB_HOST/DB_NAME/DB_USER/DB_PASSWORD — موجود
✅ REDIS_HOST/PORT       — موجود (127.0.0.1)
✅ WHATSAPP_TOKEN        — موجود
✅ TELEGRAM_BOT_TOKEN    — موجود
✅ UBERFIX_API_KEY       — موجود
```

### الخطوة 3 — قاعدة البيانات

```bash
# إنشاء الجداول (مرة واحدة)
psql -U azab_user -d alazab_core -f database/setup.sql
psql -U azab_user -d alazab_core -f database/uberfix_bot_gateway_schema.sql
```

### الخطوة 4 — التدريب

```bash
# يستغرق 20-40 دقيقة
bash scripts/botctl.sh train
```

أو مع الـ runtime domain المولّد:
```bash
bash scripts/botctl.sh validate   # تحقق أولاً
bash scripts/botctl.sh train      # ثم دربّ
```

### الخطوة 5 — التشغيل

```bash
# تشغيل كل الخدمات
bash run.sh

# أو الباك اند فقط
bash run.sh --backend

# تحقق من الحالة
bash scripts/botctl.sh status
```

### الخطوة 6 — اختبار سريع

```bash
bash scripts/botctl.sh smoke
```

---

## إذا واجهت مشكلة

```bash
# تشخيص
bash scripts/botctl.sh doctor

# إصلاح تلقائي + تنظيف منافذ
bash scripts/botctl.sh heal

# إعادة تشغيل بعد الإصلاح
bash scripts/botctl.sh restart
```

---

## مراقبة الـ logs

```bash
bash scripts/botctl.sh logs all      # كل السجلات
bash scripts/botctl.sh logs webhook  # webhook فقط
bash scripts/botctl.sh logs rasa     # Rasa فقط
bash scripts/botctl.sh logs actions  # actions فقط
```

---

## الخدمات والمنافذ

| الخدمة | المنفذ | URL |
|--------|--------|-----|
| Rasa Actions | 5055 | http://127.0.0.1:5055/health |
| Rasa Pro | 5005 | http://127.0.0.1:5005/ |
| Webhook (FastAPI) | 8000 | http://127.0.0.1:8000/health |
| Frontend (Vite) | 8080 | http://127.0.0.1:8080 |
| Admin Panel | 8000 | http://127.0.0.1:8000/static/admin/ |

---

## ترتيب التشغيل الصحيح

```
1. Redis     → يجب أن يكون شغّالاً
2. PostgreSQL → يجب أن يكون شغّالاً
3. Actions Server (5055) → يبدأ أولاً
4. Rasa Pro (5005) → يبدأ بعد Actions
5. Webhook/FastAPI (8000) → يبدأ أخيراً
6. Frontend (8080) → اختياري
```

`botctl start` يتولى هذا الترتيب تلقائياً مع health checks بين كل خطوة.

---

## Telegram Webhook (إذا لم يُسجَّل بعد)

```bash
bash scripts/register-telegram.sh
```

أو يدوياً:
```bash
curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=https://chat.alazab.com/webhook/telegram&secret_token=${TELEGRAM_WEBHOOK_SECRET}"
```

---

## Watchdog (للإنتاج)

```bash
# مراقبة تلقائية مع restart عند failure
nohup bash scripts/watchdog.sh > logs/watchdog.log 2>&1 &
```
