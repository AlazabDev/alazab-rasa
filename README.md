# AzaBot v4.0 — مجموعة العزب

بوت ذكي متكامل يخدم شرائح عملاء مجموعة العزب عبر **Rasa Pro CALM**.

---

## الخدمات

| البراند | الخدمة | الموقع |
|---------|--------|--------|
| 🏗️ Alazab Construction | مقاولات وتنفيذ مشروعات | alazab.com |
| ✨ Luxury Finishing | تشطيبات فاخرة | luxury-finishingalazab.com |
| 🎨 Brand Identity | هوية تجارية وتجهيز مساحات | brand-identityalazab.com |
| 🔧 UberFix | صيانة ذكية وتشغيل | uberfix.alazab.com |
| 🪵 Laban Alasfour | توريدات وخامات | laban-alasfour.alazab.com |

---

## البنية

```
actions/
  core/           ← DB Pool · GPT · WhatsApp (مشترك)
  brand_actions/  ← actions كل براند
  maintenance/    ← UberFix Gateway layer

webhook/
  server.py       ← 270 سطر فقط
  auth.py         ← مصادقة داخلية (4 users)
  routers/        ← admin · chat · channels
  services/       ← integrations · notifications · audio · uploads

data/
  brands/         ← flows كل براند
  general/        ← flows مشتركة (handoff · feedback · faqs)
  flows/          ← flows إضافية (maintenance · brands nav)
  nlu/            ← بيانات التدريب
```

---

## التشغيل السريع

```bash
# 1. الإعداد
make setup
# ← عدّل .env بقيمك الحقيقية

# 2. قاعدة البيانات
make db-init

# 3. التدريب (20-40 دقيقة)
make train

# 4. التشغيل
make run

# 5. اختبار
make test-chat
```

---

## المستخدمون الإداريون

```
admin@alazab.com   | devops@alazab.com
ceo@alazab.com     | mohamed@alazab.com
كلمة المرور: من .env → ADMIN_PASSWORD
```

لوحة التحكم: `http://localhost:8000/admin/`

---

## المتطلبات

- Python 3.10+
- Rasa Pro CALM license
- PostgreSQL 14+
- Redis 7+
- OpenAI API key
