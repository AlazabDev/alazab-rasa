# Ubuntu Server Setup

هذا الملف هو التسلسل الفعلي لتجهيز سيرفر Ubuntu 24.04 أو 22.04 فارغ لتشغيل `alazab-rasa` في الإنتاج.

## 1. تثبيت النظام الأساسي

على السيرفر كـ `root`:

```bash
cd /tmp
git clone <YOUR_REPO_URL> alazab-rasa-bootstrap
cd alazab-rasa-bootstrap
bash scripts/bootstrap-server-ubuntu.sh
```

نتيجة هذه الخطوة:

- تثبيت `Python`, `PostgreSQL`, `Redis`, `Nginx`, `Node 22`, `pnpm`, `certbot`
- إنشاء المستخدم `alazab`
- إنشاء المسارات:

```text
/opt/alazab-rasa/app
/opt/alazab-rasa/uploads
/opt/alazab-rasa/runtime
/etc/opt/alazab-rasa
/var/log/alazab-rasa
```

## 2. تنزيل المشروع

```bash
sudo -u alazab git clone <YOUR_REPO_URL> /opt/alazab-rasa/app
cd /opt/alazab-rasa/app
```

## 3. إنشاء قاعدة PostgreSQL محلية

استبدل القيم التالية:

- `alazab_rasa`
- `alazab_bot`
- `REPLACE_WITH_DB_PASSWORD`

ثم نفذ:

```bash
sudo -u postgres psql <<'SQL'
CREATE USER alazab_bot WITH PASSWORD 'REPLACE_WITH_DB_PASSWORD';
CREATE DATABASE alazab_rasa OWNER alazab_bot;
GRANT ALL PRIVILEGES ON DATABASE alazab_rasa TO alazab_bot;
SQL
```

اختبار الاتصال:

```bash
PGPASSWORD='REPLACE_WITH_DB_PASSWORD' psql -h 127.0.0.1 -U alazab_bot -d alazab_rasa -c 'SELECT 1;'
```

## 4. ضبط Redis بكلمة مرور

استبدل `REPLACE_WITH_REDIS_PASSWORD` ثم نفذ:

```bash
sudo cp /etc/redis/redis.conf /etc/redis/redis.conf.bak
sudo grep -qE '^#?\\s*requirepass\\s+' /etc/redis/redis.conf \
  && sudo sed -Ei 's/^#?\\s*requirepass\\s+.*/requirepass REPLACE_WITH_REDIS_PASSWORD/' /etc/redis/redis.conf \
  || echo 'requirepass REPLACE_WITH_REDIS_PASSWORD' | sudo tee -a /etc/redis/redis.conf
sudo systemctl restart redis-server
redis-cli -a REPLACE_WITH_REDIS_PASSWORD ping
```

يجب أن تعيد:

```text
PONG
```

## 5. تجهيز ملف البيئة

```bash
sudo cp /opt/alazab-rasa/app/deploy/production/.env.bot.alazab.example /etc/opt/alazab-rasa/.env
sudo chown root:alazab /etc/opt/alazab-rasa/.env
sudo chmod 640 /etc/opt/alazab-rasa/.env
sudo nano /etc/opt/alazab-rasa/.env
```

الحد الأدنى الذي يجب ملؤه داخل `.env`:

- `RASA_PRO_LICENSE`
- `OPENAI_API_KEY`
- `PUBLIC_BASE_URL=https://bot.alazab.com`
- `ALLOWED_ORIGINS=https://bot.alazab.com,...`
- `DB_HOST=127.0.0.1`
- `DB_PORT=5432`
- `DB_NAME=alazab_rasa`
- `DB_USER=alazab_bot`
- `DB_PASSWORD=...`
- `REDIS_HOST=127.0.0.1`
- `REDIS_PORT=6379`
- `REDIS_PASSWORD=...`
- `ADMIN_EMAIL=admin@alazab.com`
- `ADMIN_PASSWORD=...`
- `ADMIN_SESSION_SECRET=...`
- `UPLOADS_DIR=/opt/alazab-rasa/uploads`
- `ADMIN_DATA_FILE=/opt/alazab-rasa/runtime/admin-data.json`
- `UPLOADS_PUBLIC_ENABLED=false`

## 6. نشر المشروع

نفذ كالمستخدم `alazab`:

```bash
sudo -u alazab bash -lc '
cd /opt/alazab-rasa/app &&
bash scripts/deploy-server-nodocker.sh \
  --env-file /etc/opt/alazab-rasa/.env \
  --branch main \
  --configure-nginx \
  --domain bot.alazab.com
'
```

## 7. إصدار شهادة SSL

بعد توجيه DNS إلى السيرفر:

```bash
sudo certbot --nginx -d bot.alazab.com
sudo nginx -t && sudo systemctl reload nginx
```

## 8. Smoke test بعد النشر

```bash
curl -fsS http://127.0.0.1:5005/
curl -fsS http://127.0.0.1:8000/health
curl -I https://bot.alazab.com
sudo systemctl status alazab-rasa-actions --no-pager
sudo systemctl status alazab-rasa-rasa --no-pager
sudo systemctl status alazab-rasa-webhook --no-pager
```

اختبار الدخول الإداري:

```bash
curl -fsS -X POST https://bot.alazab.com/admin/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@alazab.com","password":"REPLACE_WITH_ADMIN_PASSWORD"}'
```

## 9. مسار أسرع

لو تريد تنفيذًا شبه كامل بعد مراجعة المتغيرات مرة واحدة:

```bash
cd /opt/alazab-rasa/app
cp deploy/production/first-deploy.example.sh /root/first-deploy.sh
nano /root/first-deploy.sh
bash /root/first-deploy.sh
```
