# Production Deployment Blueprint

هذا المسار هو المرجع المختصر لنشر `alazab-rasa` على سيرفر Linux بدون Supabase كاعتماد أساسي.

لإعداد سيرفر Ubuntu من الصفر راجع:
[deploy/production/server-setup.md](A:/a/chatbot/alazab-rasa/deploy/production/server-setup.md)

ولنموذج البيئة الجاهز للدومين الحالي:
[deploy/production/.env.bot.alazab.example](A:/a/chatbot/alazab-rasa/deploy/production/.env.bot.alazab.example)

ولمسار نشر أولي شبه جاهز:
[deploy/production/first-deploy.example.sh](A:/a/chatbot/alazab-rasa/deploy/production/first-deploy.example.sh)

## المسارات المقترحة

```text
/opt/alazab-rasa/app
/opt/alazab-rasa/uploads
/opt/alazab-rasa/runtime/admin-data.json
/etc/opt/alazab-rasa/.env
```

## قبل أول نشر

1. انسخ المشروع إلى `/opt/alazab-rasa/app`
2. انسخ [deploy/production/.env.example](A:\a\chatbot\alazab-rasa\deploy\production\.env.example) إلى `/etc/opt/alazab-rasa/.env`
3. استبدل كل القيم التجريبية بقيم حقيقية
4. تأكد أن:
   - `PUBLIC_BASE_URL=https://bot.alazab.com`
   - `RASA_URL=http://127.0.0.1:5005`
   - `ACTION_SERVER_URL=http://127.0.0.1:5055/webhook`
   - `UPLOADS_PUBLIC_ENABLED=false`

## الحد الأدنى المطلوب ليعمل البوت

لا تترك هذه القيم فارغة:

- `RASA_PRO_LICENSE`
- `OPENAI_API_KEY`
- `PUBLIC_BASE_URL`
- `ALLOWED_ORIGINS`
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`
- `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `ADMIN_SESSION_SECRET`
- `UPLOADS_DIR`, `ADMIN_DATA_FILE`

ويمكن ترك هذه القيم فارغة إذا لم تكن القنوات مفعلة:

- `WHATSAPP_API_URL`, `WHATSAPP_TOKEN`, `FB_*`
- `TELEGRAM_BOT_TOKEN`
- `WEBHOOK_NOTIFY_URL`, `NOTIFY_PHONE`, `NOTIFY_TG_CHAT_ID`
- `UBERFIX_*` إذا لم تكن مسارات UberFix مستخدمة على هذا السيرفر

## النشر

من داخل المشروع:

```bash
cp deploy/production/nginx/bot.alazab.com.conf /etc/nginx/sites-available/bot.alazab.com
ln -sfn /etc/nginx/sites-available/bot.alazab.com /etc/nginx/sites-enabled/bot.alazab.com
nginx -t && systemctl reload nginx

bash scripts/deploy-server-nodocker.sh \
  --env-file /etc/opt/alazab-rasa/.env \
  --branch main \
  --configure-nginx \
  --domain bot.alazab.com
```

## التحقق بعد النشر

```bash
curl -fsS http://127.0.0.1:5005/
curl -fsS http://127.0.0.1:8000/health
curl -I https://bot.alazab.com
systemctl status alazab-rasa-actions --no-pager
systemctl status alazab-rasa-rasa --no-pager
systemctl status alazab-rasa-webhook --no-pager
```

## المرفقات والإدارة

- ملفات المستخدمين تخزن محليًا في `UPLOADS_DIR`
- واجهة الإدارة تعرضها عبر روابط إدارية محمية: `/admin/uploads/{id}/download`
- لا تفعّل `UPLOADS_PUBLIC_ENABLED=true` إلا لو كنت تقصد نشر الملفات للعامة
