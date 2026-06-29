# 🚀 خطوات التصطيب والتشغيل — AzaBot

دليل تنفيذي مرتّب: من جهازك المحلي (WSL) → الإنتاج على السيرفر.

---

## 🖥️ الجزء 1: التطوير المحلي (WSL / جهازك)

### الخطوة 0 — تأكد من المكان الصحيح
```bash
# ⚠️ لا تشتغل من /mnt/d/... (قرص ويندوز) — بطيء جداً مع rasa-pro
# انقل المشروع لـ Linux filesystem جوّه WSL أولاً:
mkdir -p ~/prod && cd ~/prod
mv /mnt/d/site/chatbot/alazab-rasa-prod .
cd alazab-rasa-prod
```

### الخطوة 1 — تثبيت uv (مرة واحدة فقط، اختياري لكن موصى به)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc   # أو افتح terminal جديد
uv --version       # تأكيد التثبيت
```

### الخطوة 2 — الإعداد الكامل
```bash
chmod +x az.sh
bash az.sh setup
```
ده بيعمل: تثبيت Python (rasa-pro أولاً، باقي الحزم تانياً) + إنشاء `.env` من القالب + تثبيت الفرونت.

### الخطوة 3 — تعبئة `.env`
```bash
nano .env
```
أهم المتغيرات المطلوبة:
```
OPENAI_API_KEY=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
DB_HOST=...
DB_PASSWORD=...
REDIS_HOST=127.0.0.1
ADMIN_SESSION_SECRET=        # يُولَّد في الخطوة التالية
```

### الخطوة 4 — توليد كلمات مرور الأدمن
```bash
bash az.sh passwd
```
انسخ كل السطور الناتجة (`ADMIN_PASSWORD_HASH_*` و `ADMIN_SESSION_SECRET`) وحطّها في `.env`.

### الخطوة 5 — تثبيت وتشغيل Redis (لو غير موجود)
```bash
sudo apt-get update && sudo apt-get install -y redis-server
sudo systemctl enable --now redis-server
redis-cli ping   # يجب أن يرجع PONG
```

### الخطوة 6 — فحص شامل قبل التشغيل
```bash
bash az.sh doctor
```
يجب أن تكون كل الأسطر `[ok]`. لو فيه `[warn]` لـ `ADMIN_PASSWORD_HASH_ADMIN` راجع الخطوة 4.

### الخطوة 7 — تهيئة قاعدة البيانات (مرة واحدة فقط)
```bash
bash az.sh db-init
```

### الخطوة 8 — تحقق من بيانات Rasa (segments + flows + domain)
```bash
bash az.sh validate
```

### الخطوة 9 — تدريب أول نموذج
```bash
NODE_ENV=dev bash az.sh train
```
⚠️ لاحظ `NODE_ENV=dev` — التدريب محظور تلقائياً لو `NODE_ENV=production` في `.env`.

### الخطوة 10 — التشغيل المحلي
```bash
bash az.sh on
bash az.sh status     # تأكيد أن الثلاث خدمات شغّالة
bash az.sh smoke      # اختبار سريع لـ /health و /chat
```

### أثناء التطوير
```bash
bash az.sh logs webhook    # تتبّع لوجز خدمة معينة
bash az.sh restart         # بعد أي تعديل كود
bash az.sh heal            # لو بورت عالق أو عملية متجمدة
bash az.sh off             # نهاية الجلسة
```

---

## 🌐 الجزء 2: النشر للإنتاج (سيرفر Ubuntu)

### المتطلبات قبل البدء
- سيرفر Ubuntu 22.04/24.04 بصلاحية root/sudo
- دومين مُوجَّه للسيرفر (A record) — مثلاً `bot.alazab.com`
- نفس قيم `.env` اللي جهّزتها محلياً (لكن بقيم إنتاج حقيقية، و`NODE_ENV=production`)

### الخطوة 1 — رفع المشروع للسيرفر
```bash
# من جهازك المحلي
scp -r alazab-rasa-prod user@server-ip:/home/user/
ssh user@server-ip
```

### الخطوة 2 — تجهيز السيرفر من الصفر (حزم النظام)
```bash
cd alazab-rasa-prod
sudo bash deploy/production/server-setup.sh
```
يثبّت: Python, Nginx, Redis, Certbot, وكل متطلبات النظام.

### الخطوة 3 — `.env` للإنتاج
```bash
cp .env.example .env
nano .env
```
**تأكد من:**
```
NODE_ENV=production
TRAIN_ON_DEPLOY=false
PUBLIC_BASE_URL=https://bot.alazab.com
ALLOWED_ORIGINS=https://alazab.com,https://bot.alazab.com,...
```

### الخطوة 4 — كلمات المرور + الإعداد
```bash
bash az.sh passwd      # أضف الناتج لـ .env
bash az.sh setup       # تثبيت الحزم على السيرفر
bash az.sh doctor      # فحص أخير
bash az.sh check       # فحص جاهزية الإنتاج (prod-check.sh)
```

### الخطوة 5 — قاعدة البيانات
```bash
bash az.sh db-init
```

### الخطوة 6 — النموذج
⛔ **لا تدرّب على السيرفر مباشرة.** درّب محلياً وارفع النموذج الجاهز:
```bash
# على جهازك المحلي:
NODE_ENV=dev bash az.sh release      # validate + train + build + check
scp models/alazab-*.tar.gz user@server-ip:~/alazab-rasa-prod/models/
```

### الخطوة 7 — النشر الكامل (nginx + systemd + SSL)
```bash
sudo bash az.sh deploy
```
هذا الأمر (يستدعي `deploy/production/deploy-production.sh`) يعمل:
- إنشاء مستخدم نظام مخصص (`azab`)
- نسخ الملفات لـ `/opt/azabot` (بدون `.env`/`ssl`/أسرار)
- بناء venv + تثبيت الحزم
- تركيب وحدات `systemd` (`azabot-actions`, `azabot-rasa`, `azabot-webhook`)
- تركيب وتفعيل إعدادات Nginx
- smoke test نهائي على `/health`

### الخطوة 8 — شهادة SSL
```bash
sudo certbot --nginx -d bot.alazab.com -d www.bot.alazab.com
sudo certbot renew --dry-run    # تأكيد أن التجديد التلقائي يعمل
```

### الخطوة 9 — التأكيد النهائي
```bash
bash az.sh status                          # يكتشف systemd تلقائياً
curl -s https://bot.alazab.com/health      # يجب: {"status":"ok",...}
sudo systemctl status azabot-webhook azabot-rasa azabot-actions
```

---

## 🔄 الجزء 3: دورة التحديث المستمر (بعد أول نشر)

### تحديث الكود فقط (بدون نموذج جديد)
```bash
# محلياً
git push   # أو scp يدوي
# على السيرفر
ssh user@server-ip
cd alazab-rasa-prod && git pull
sudo bash az.sh deploy        # يعيد البناء والنشر
```

### تحديث النموذج فقط
```bash
# محلياً
NODE_ENV=dev bash az.sh release
scp models/alazab-*.tar.gz user@server-ip:/opt/azabot/models/
ssh user@server-ip "sudo systemctl restart azabot-rasa"
```

### تشخيص مشكلة في الإنتاج
```bash
bash az.sh logs webhook
sudo journalctl -u azabot-rasa -n 100 --no-pager
bash az.sh status
redis-cli ping
```

---

## ⚡ الترتيب الكامل (نسخ-لصق سريع) — تطوير محلي

```bash
chmod +x az.sh
bash az.sh setup
nano .env
bash az.sh passwd        # أضف الناتج لـ .env يدوياً
sudo systemctl enable --now redis-server
bash az.sh doctor
bash az.sh db-init
bash az.sh validate
NODE_ENV=dev bash az.sh train
bash az.sh on
bash az.sh status
bash az.sh smoke
```

## ⚡ الترتيب الكامل (نسخ-لصق سريع) — نشر إنتاج

```bash
sudo bash deploy/production/server-setup.sh
cp .env.example .env && nano .env     # NODE_ENV=production
bash az.sh passwd
bash az.sh setup && bash az.sh check
bash az.sh db-init
# (النموذج يُرفَع من جهاز التطوير — راجع الجزء 2 خطوة 6)
sudo bash az.sh deploy
sudo certbot --nginx -d bot.alazab.com
bash az.sh status
```
