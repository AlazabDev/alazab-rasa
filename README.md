# AzaBot v4.0 — مجموعة العزب

بوت ذكي متكامل يخدم شرائح عملاء مجموعة العزب عبر **Rasa Pro CALM**.

---

## الخدمات

| البراند | الخدمة | الموقع |
|---------|--------|--------|
| 🏗️ Alazab Construction | مقاولات وتنفيذ مشروعات | alazab.com |
| ✨ Luxury Finishing | تشطيبات فاخرة | luxury-finishing.alazab.com |
| 🎨 Brand Identity | هوية تجارية وتجهيز مساحات | brand-identity.alazab.com |
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

## التشغيل السريع (التطوير)

```bash
# 1. الإعداد
bash az.sh setup
# ← عدّل .env بقيمك الحقيقية

# 2. إعداد قاعدة البيانات (في حال الحاجة)
bash az.sh db-init

# 3. تدريب النموذج
bash az.sh train

# 4. تشغيل جميع الخدمات (Backend + Frontend)
bash az.sh dev

# 5. اختبار النظام
bash az.sh smoke
```

---

## التشغيل في بيئة الإنتاج (Production)

```bash
# فحص جاهزية الإنتاج
bash az.sh prod-preflight

# تشغيل حاويات الإنتاج
bash az.sh prod-up

# إيقاف التشغيل
bash az.sh prod-down
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
