# إعداد خادم الإنتاج — AzaBot / مجموعة العزب

## المتطلبات
- Ubuntu 22.04 LTS
- 4 vCPU / 8 GB RAM (الحد الأدنى)
- Python 3.11
- Node.js 22+ + pnpm
- Nginx
- Redis Cloud (مضبوط في .env)
- PostgreSQL (محلي أو بعيد)

## خطوات الإعداد الأولي (مرة واحدة)

```bash
# 1. تحديث النظام
sudo apt update && sudo apt upgrade -y

# 2. تثبيت Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev build-essential

# 3. تثبيت Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g pnpm

# 4. تثبيت Nginx
sudo apt install -y nginx certbot python3-certbot-nginx

# 5. شهادة SSL (Let's Encrypt)
sudo certbot --nginx -d bot.alazab.com -d www.bot.alazab.com

# 6. إعداد ملف .env في /opt/azabot/.env
#    انسخ المتغيرات من .env المحلي

# 7. تشغيل السكريبت
sudo bash deploy/production/deploy-production.sh
```

## أوامر الإدارة اليومية

```bash
# الحالة
bash scripts/botctl.sh status

# السجلات
journalctl -u azabot-webhook -f
journalctl -u azabot-rasa -f
journalctl -u azabot-actions -f

# إعادة تشغيل
sudo systemctl restart azabot-webhook
sudo systemctl restart azabot-rasa
sudo systemctl restart azabot-actions

# نشر تحديث
sudo bash deploy/production/deploy-production.sh
```

## نقاط المراقبة

| الخدمة | المنفذ | health check |
|--------|--------|-------------|
| Webhook (FastAPI) | 8000 | `curl http://127.0.0.1:8000/health` |
| Rasa Pro | 5005 | `curl http://127.0.0.1:5005/` |
| Actions | 5055 | `curl http://127.0.0.1:5055/health` |
