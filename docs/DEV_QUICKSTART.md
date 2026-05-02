# 🚀 DEV QUICKSTART — AzaBot

## التشغيل الكامل بأمر واحد

```bash
# 1. أضف بياناتك
cp .env.example .env
nano .env          # أضف RASA_PRO_LICENSE, OPENAI_API_KEY, DB_, REDIS_

# 2. جهّز البيئة وتدرّب مرة واحدة
bash scripts/botctl.sh setup   # إنشاء venv وتثبيت packages
bash scripts/botctl.sh train   # تدريب موديل Rasa

# 3. شغّل كل شيء
bash dev.sh
```

## المنافذ

| الخدمة | المنفذ | URL |
|--------|--------|-----|
| 🌐 الواجهة (React+Vite) | 8080 | http://localhost:8080 |
| ⚙️  Webhook API (FastAPI) | 8000 | http://localhost:8000 |
| 📖 API Docs | 8000 | http://localhost:8000/docs |
| 🤖 Rasa Pro | 5005 | http://localhost:5005 |
| 🔧 Actions Server | 5055 | http://localhost:5055 |

## أوامر dev.sh

```bash
bash dev.sh                  # تشغيل كل شيء
bash dev.sh --backend        # باك اند فقط
bash dev.sh --frontend       # فرونت فقط
bash dev.sh stop             # إيقاف كل شيء
bash dev.sh restart          # إعادة تشغيل
bash dev.sh status           # حالة الخدمات
bash dev.sh logs all         # كل السجلات
bash dev.sh logs frontend    # سجلات الفرونت
bash dev.sh logs webhook     # سجلات FastAPI
bash dev.sh logs rasa        # سجلات Rasa
bash dev.sh logs actions     # سجلات Actions
```

## بديل: make commands

```bash
make dev          # تشغيل كل شيء
make dev-stop     # إيقاف
make dev-status   # الحالة
make dev-logs     # السجلات
make dev-backend  # باك فقط
make dev-frontend # فرونت فقط
make dev-restart  # إعادة تشغيل
```

## الـ Proxy (مضبوط تلقائياً)

Vite proxy مضبوط في `azabot/vite.config.ts` — كل طلبات `/chat /brands /admin /health ...`
تُحوَّل تلقائياً للباك اند على port 8000. **لا حاجة لأي إعداد إضافي.**

## تدريب الموديل (عند تغيير ملفات data/)

```bash
bash scripts/botctl.sh train
# ثم أعد تشغيل الباك اند
bash dev.sh restart
```
