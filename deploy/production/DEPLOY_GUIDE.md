# 🚀 دليل نشر AzaBot — bot.alazab.com
### الخادم: 2 vCPU / 8 GB RAM / Ubuntu 22.04

---

## قبل البدء — تأكد من جاهزية هذه القيم

```
✅ RASA_PRO_LICENSE   = __REMOVED_FROM_GIT_HISTORY__
✅ OPENAI_API_KEY     = sk-proj-...
✅ REDIS_HOST         = redis host
✅ REDIS_PASSWORD     = ...
✅ DB_HOST            = db host أو Supabase
✅ ADMIN_PASSWORD     = كلمة سر قوية
✅ DNS A Record       = bot.alazab.com → Server IP
```

---

## الخطوة 1 — رفع المشروع للسيرفر

```bash
# من جهازك المحلي
scp alazab-rasa-FINAL.zip user@SERVER_IP:~
ssh user@SERVER_IP

# على السيرفر
cd ~
unzip alazab-rasa-FINAL.zip -d /opt
mv /opt/alazab-rasa-prod /opt/azabot
cd /opt/azabot
```

---

## الخطوة 2 — إعداد السيرفر (مرة واحدة)

```bash
# يثبّت: Python 3.11, Node 22, pnpm, Nginx, Redis, PostgreSQL
# يضيف: 4GB Swap، Firewall، SSL
sudo bash deploy/production/server-setup.sh
```

**ما يفعله تلقائياً:**
| الأداة | الإجراء |
|--------|---------|
| Swap 4GB | حماية الخادم من OOM عند تحميل Rasa |
| UFW Firewall | فتح 80/443 فقط — إغلاق 5005/5055/8000 |
| Redis | maxmemory 256MB + allkeys-lru |
| SSL | Let's Encrypt عبر certbot |
| Nginx | worker_processes 2 + buffers مُحسَّنة |

---

## الخطوة 3 — إضافة Credentials

```bash
cp .env.example .env
nano .env
```

**المتغيرات المطلوبة حتماً:**
```env
RASA_PRO_LICENSE=__REMOVED_FROM_GIT_HISTORY__
OPENAI_API_KEY=sk-proj-...
ADMIN_PASSWORD=كلمة-سر-قوية-16+-حرف
ADMIN_SESSION_SECRET=base64-32-bytes
DB_HOST=127.0.0.1   # أو Supabase URL
DB_PASSWORD=...
REDIS_HOST=127.0.0.1  # أو Redis Cloud
REDIS_PASSWORD=...
ALLOWED_ORIGINS=https://bot.alazab.com,https://alazab.com
PUBLIC_BASE_URL=https://bot.alazab.com
```

**توليد ADMIN_SESSION_SECRET:**
```bash
openssl rand -base64 32
```

---

## الخطوة 4 — تدريب الموديل

```bash
# يأخذ 5–15 دقيقة على 2 vCPU
bash scripts/botctl.sh train
```

---

## الخطوة 5 — النشر

```bash
sudo bash deploy/production/deploy-production.sh
```

**ما يفعله:**
1. إنشاء system user `azab`
2. مزامنة الملفات إلى `/opt/azabot`
3. Python venv + packages
4. بناء React frontend (`pnpm build`)
5. تثبيت 3 systemd services
6. تثبيت Nginx config
7. تشغيل الخدمات وإعادة تحميل Nginx
8. Smoke test تلقائي

---

## الخطوة 6 — التحقق

```bash
# Health check
curl https://bot.alazab.com/health

# الحالة
sudo systemctl status azabot-webhook azabot-rasa azabot-actions

# السجلات
journalctl -u azabot-rasa -f
journalctl -u azabot-webhook -f

# استهلاك الموارد (مهم على 2 vCPU)
htop
free -h
```

---

## توزيع الموارد على 2 vCPU / 8 GB

```
الخدمة          | CPU      | RAM
─────────────────|──────────|──────────
Rasa Pro        | 80%      | 6 GB max
azabot-webhook  | 40%      | 512 MB
azabot-actions  | 30%      | 512 MB
Nginx           | ~5%      | ~50 MB
Redis           | ~5%      | 256 MB
PostgreSQL      | ~10%     | ~200 MB
OS              | base     | ~300 MB
─────────────────|──────────|──────────
Swap (احتياطي)  | —        | 4 GB
```

> **ملاحظة:** CPUQuota في systemd لا تتراكم — Rasa يأخذ 80% فقط عند الحاجة، وتترك النوى الباقية لبقية الخدمات.

---

## التحديث (deploy بعد تعديلات)

```bash
# إذا غيّرت ملفات data/ فقط
bash scripts/botctl.sh train
sudo systemctl restart azabot-rasa

# إذا غيّرت الكود
sudo bash deploy/production/deploy-production.sh

# إذا غيّرت الفرونت فقط
bash azabot/scripts/build-production.sh
sudo systemctl reload nginx
```

---

## مراقبة الخادم يومياً

```bash
# استهلاك الذاكرة (مهم مع Rasa)
free -h && swapon --show

# إذا امتلأ الـ swap
sudo systemctl restart azabot-rasa   # يُعيد تحميل الموديل

# سجلات الأخطاء
journalctl -u azabot-rasa --since "1 hour ago" | grep -i error
tail -50 /var/log/nginx/bot_alazab_error.log
```

---

## مشاكل شائعة وحلولها

| المشكلة | الحل |
|---------|------|
| Rasa لا يبدأ (OOM) | `sudo bash deploy/production/setup-swap.sh` |
| 502 Bad Gateway | `sudo systemctl restart azabot-rasa azabot-webhook` |
| SSL منتهي | `sudo certbot renew` |
| 429 Too Many Requests | طبيعي — rate limiting يعمل |
| الموديل قديم | `bash scripts/botctl.sh train && sudo systemctl restart azabot-rasa` |
