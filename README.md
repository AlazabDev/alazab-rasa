<div align="center">

# 🤖 AzaBot — مجموعة العزب الذكي

**Rasa Pro CALM · Python FastAPI · React 18 · Arabic NLU**

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Rasa](https://img.shields.io/badge/Rasa-Pro_3.16-purple)](https://rasa.com)
[![React](https://img.shields.io/badge/React-18-61dafb)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)](https://fastapi.tiangolo.com)

</div>

---

## البراندات المدعومة

| البراند | الخدمة | النطاق |
|---------|--------|--------|
| 🏢 Alazab Construction | مقاولات وبناء | alazab.com |
| ✨ Luxury Finishing | تشطيبات فاخرة | luxury.alazab.com |
| 🎨 Brand Identity | هوية تجارية | brand.alazab.com |
| 🔧 UberFix | صيانة منزلية | uberfix.shop |
| 🌿 Laban Alasfour | توريدات ألبان | labanalasfour.com |

---

## التشغيل السريع (WSL / Linux)

```bash
# 1. إعداد البيئة (مرة واحدة)
bash wsl-setup.sh

# 2. أضف الـ credentials
nano .env   # RASA_PRO_LICENSE + OPENAI_API_KEY

# 3. تدريب الموديل
bash scripts/botctl.sh train

# 4. تشغيل كل شيء
bash dev.sh
```

**بعدها:** http://localhost:8080

---

## النشر على الإنتاج (bot.alazab.com)

```bash
# على السيرفر (مرة واحدة)
sudo bash deploy/production/server-setup.md   # راجع الملف أولاً

# نشر / تحديث
sudo bash deploy/production/deploy-production.sh
```

---

## البنية التقنية

```
المستخدم
    │
    ▼ HTTPS
  Nginx (bot.alazab.com)
    │
    ├── /assets/ → azabot/dist/ (React SPA, immutable cache)
    │
    ├── /chat → FastAPI :8000
    ├── /admin → FastAPI :8000
    └── /* → React SPA (index.html)

FastAPI :8000
    │
    └── Rasa Pro :5005
            │
            └── Actions Server :5055
```

---

## أوامر رئيسية

```bash
bash dev.sh                   # تشغيل كل شيء
bash dev.sh stop              # إيقاف
bash dev.sh status            # الحالة
bash dev.sh logs all          # السجلات
bash scripts/botctl.sh train  # تدريب الموديل
make help                     # كل الأوامر
```

---

## المنافذ

| الخدمة | المنفذ |
|--------|--------|
| Frontend (Vite dev) | 8080 |
| Webhook API (FastAPI) | 8000 |
| Rasa Pro | 5005 |
| Actions Server | 5055 |


Metadata-Version: 2.4
Name: alazab-group-rasa-bot
Version: 2.0.0
Summary: Rasa Pro CALM chatbot for Alazab Group — 5 brands, Arabic NLU, LLM-powered
Requires-Python: >=3.10
Description-Content-Type: text/markdown
License-File: LICENSE
Requires-Dist: rasa-pro>=3.16
Requires-Dist: rasa-sdk>=3.16
Requires-Dist: fastapi>=0.110.0
Requires-Dist: uvicorn[standard]>=0.29.0
Requires-Dist: httpx>=0.27.0
Requires-Dist: python-dotenv>=1.0.0
Requires-Dist: python-multipart>=0.0.9
Requires-Dist: pydantic>=2.0.0
Requires-Dist: openai>=1.0.0
Requires-Dist: psycopg[binary]>=3.2.0
Provides-Extra: dev
Requires-Dist: pytest>=8.0.0; extra == "dev"
Requires-Dist: ruff>=0.4.0; extra == "dev"
Dynamic: license-file

<div align="center">

# 🤖 AzaBot — مجموعة العزب الذكي

**Rasa Pro CALM · Python FastAPI · React 18 · Arabic NLU**

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Rasa](https://img.shields.io/badge/Rasa-Pro_3.16-purple)](https://rasa.com)
[![React](https://img.shields.io/badge/React-18-61dafb)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)](https://fastapi.tiangolo.com)

</div>

---

## البراندات المدعومة

| البراند | الخدمة | النطاق |
|---------|--------|--------|
| 🏢 Alazab Construction | مقاولات وبناء | alazab.com |
| ✨ Luxury Finishing | تشطيبات فاخرة | luxury.alazab.com |
| 🎨 Brand Identity | هوية تجارية | brand.alazab.com |
| 🔧 UberFix | صيانة منزلية | uberfix.shop |
| 🌿 Laban Alasfour | توريدات ألبان | labanalasfour.com |

---

## التشغيل السريع (WSL / Linux)

```bash
# 1. إعداد البيئة (مرة واحدة)
bash wsl-setup.sh

# 2. أضف الـ credentials
nano .env   # RASA_PRO_LICENSE + OPENAI_API_KEY

# 3. تدريب الموديل
bash scripts/botctl.sh train

# 4. تشغيل كل شيء
bash dev.sh
```

**بعدها:** http://localhost:8080

---

## النشر على الإنتاج (bot.alazab.com)

```bash
# على السيرفر (مرة واحدة)
sudo bash deploy/production/server-setup.md   # راجع الملف أولاً

# نشر / تحديث
sudo bash deploy/production/deploy-production.sh
```

---

## البنية التقنية

```
المستخدم
    │
    ▼ HTTPS
  Nginx (bot.alazab.com)
    │
    ├── /assets/ → azabot/dist/ (React SPA, immutable cache)
    │
    ├── /chat → FastAPI :8000
    ├── /admin → FastAPI :8000
    └── /* → React SPA (index.html)

FastAPI :8000
    │
    └── Rasa Pro :5005
            │
            └── Actions Server :5055
```

---

## أوامر رئيسية

```bash
bash dev.sh                   # تشغيل كل شيء
bash dev.sh stop              # إيقاف
bash dev.sh status            # الحالة
bash dev.sh logs all          # السجلات
bash scripts/botctl.sh train  # تدريب الموديل
make help                     # كل الأوامر
```

---

## المنافذ

| الخدمة | المنفذ |
|--------|--------|
| Frontend (Vite dev) | 8080 |
| Webhook API (FastAPI) | 8000 |
| Rasa Pro | 5005 |
| Actions Server | 5055 |
