# 🪟 دليل الاختبار على WSL — AzaBot

## المتطلبات

| المطلوب | الإصدار | ملاحظة |
|---------|---------|--------|
| Windows 11 / 10 | - | WSL2 مفعّل |
| Ubuntu WSL | 22.04 LTS | مُوصى به |
| RAM | 8 GB+ | Rasa ثقيل على الذاكرة |
| Python | 3.11 | يُثبَّت تلقائياً |
| Node.js | 22+ | يُثبَّت تلقائياً |

---

## الإعداد (مرة واحدة)

### 1. افتح WSL وانتقل للمشروع
```bash
cd /mnt/c/Users/<اسمك>/projects/alazab-rasa
# أو
cd ~/alazab-rasa
```

### 2. ضبط الذاكرة (مهم لـ Rasa)
```
# في Windows PowerShell:
notepad $env:USERPROFILE\.wslconfig
```
انسخ محتوى ملف `.wslconfig.recommended` ثم:
```powershell
wsl --shutdown
# افتح WSL من جديد
```

### 3. الإعداد التلقائي
```bash
bash wsl-setup.sh
```
سيُثبّت ويُعدّ:
- Python 3.11 + venv
- Node.js 22 + pnpm
- Redis (محلي)
- PostgreSQL (محلي)
- .env بقيم افتراضية للـ dev
- Frontend packages

### 4. أضف License و API Key
```bash
nano .env
```
غيّر:
```
RASA_PRO_LICENSE=__REMOVED_FROM_GIT_HISTORY__
OPENAI_API_KEY=<مفتاحك الفعلي>
```

### 5. تدريب الموديل
```bash
bash scripts/botctl.sh train
# يأخذ 5–15 دقيقة حسب الجهاز
```

### 6. الاختبار
```bash
bash wsl-test.sh          # اختبار شامل مع تشغيل خدمات
bash wsl-test.sh --quick  # اختبار سريع بدون تشغيل خدمات
```

### 7. التشغيل الكامل
```bash
bash dev.sh
```

---

## URLs بعد التشغيل

| الخدمة | URL |
|--------|-----|
| 🌐 الواجهة | http://localhost:8080 |
| ⚙️ API | http://localhost:8000 |
| 📖 API Docs | http://localhost:8000/docs |
| 🔧 Admin | http://localhost:8000/admin |

---

## أوامر شائعة

```bash
bash dev.sh stop             # إيقاف كل شيء
bash dev.sh status           # الحالة
bash dev.sh logs frontend    # سجلات الفرونت
bash dev.sh logs webhook     # سجلات API
bash dev.sh logs rasa        # سجلات Rasa
bash dev.sh restart          # إعادة تشغيل

# تدريب بعد تعديل data/
bash scripts/botctl.sh train && bash dev.sh restart
```

---

## مشاكل شائعة وحلولها

### ❌ `Port 8000 is already in use`
```bash
bash dev.sh stop
# أو
lsof -i :8000 | awk 'NR>1{print $2}' | xargs kill -9
```

### ❌ `Redis connection refused`
```bash
sudo service redis-server start
redis-cli ping  # يجب أن يرجع: PONG
```

### ❌ `PostgreSQL connection failed`
```bash
sudo service postgresql start
psql -U azab_user -d alazab_core -h 127.0.0.1
```

### ❌ `Out of memory` عند تدريب Rasa
تأكد من `.wslconfig` مع `memory=8GB`، ثم:
```powershell
wsl --shutdown
```

### ❌ سكريبت يعطي `\r: bad interpreter`
```bash
dos2unix dev.sh scripts/botctl.sh wsl-setup.sh wsl-test.sh
```

---

## الفرق بين WSL dev والإنتاج

| الجانب | WSL Dev | Production (Linux) |
|--------|---------|-------------------|
| قاعدة البيانات | PostgreSQL محلي | Cloud / Remote |
| Redis | Redis محلي بدون password | Redis Cloud مع SSL |
| Frontend | Vite dev server (HMR) | `pnpm build` → nginx |
| التشغيل | `bash dev.sh` | systemd services |
| HTTPS | بدون SSL | Let's Encrypt |
