# 📘 دليل أوامر AzaBot — az.sh هو المصدر الوحيد

> ⚠️ **لا Make. لا Docker.** كل التشغيل والبناء والتدريب والنشر يمر عبر `az.sh` فقط.
> يستخدم `uv` كمدير حزم أساسي (أسرع وأكثر استقراراً مع rasa-pro)، مع تراجع تلقائي لـ pip+venv لو uv غير متاح.

---

## ⚡ البداية السريعة

```bash
chmod +x az.sh

bash az.sh setup     # تثبيت كامل: Python (uv/pip) + .env + الفرونت
bash az.sh doctor    # فحص شامل للبيئة
bash az.sh passwd    # توليد bcrypt hashes لكلمات مرور الأدمن
bash az.sh on        # تشغيل actions + rasa + webhook
bash az.sh status    # تأكيد أنها تعمل
```

---

## 📋 كل الأوامر

### الإعداد
| أمر | الوظيفة |
|---|---|
| `az.sh setup` | تثبيت كامل (Python + .env + frontend) — نقطة البداية الوحيدة |
| `az.sh install` | تثبيت حزم Python فقط (بدون .env/frontend) |
| `az.sh doctor` | فحص uv/python/venv/.env/redis |
| `az.sh check` | فحص جاهزية الإنتاج الشامل |

### التشغيل
| أمر | الوظيفة |
|---|---|
| `az.sh on` | تشغيل الخدمات الثلاث (يكتشف systemd تلقائياً في الإنتاج) |
| `az.sh off` | إيقافها |
| `az.sh restart` | إعادة تشغيل |
| `az.sh status` | حالة كل خدمة + health check |
| `az.sh logs [service]` | تتبّع اللوجز (افتراضي: webhook) |
| `az.sh smoke` | اختبار سريع لـ /health و /chat |
| `az.sh heal` | تحرير بورتات عالقة + تنظيف PID files |

### قاعدة البيانات
| أمر | الوظيفة |
|---|---|
| `az.sh db-init` | تنفيذ `database/setup.sql` |

### دورة حياة Rasa والإنتاج
| أمر | الوظيفة |
|---|---|
| `az.sh validate` | `rasa data validate` (بدون تدريب) |
| `az.sh train [--force]` | تدريب — **محظور تلقائياً في `NODE_ENV=production`** إلا بـ `--force` |
| `az.sh test` | `rasa test` (E2E) |
| `az.sh build` | تحقق + بناء الفرونت + عرض آخر نموذج جاهز |
| `az.sh release [--force]` | **الكل دفعة واحدة:** validate → train → build → check |

### الأمان
| أمر | الوظيفة |
|---|---|
| `az.sh passwd` | توليد bcrypt hash لكل مستخدمي الأدمن |
| `az.sh untrack` | إزالة الملفات الحساسة من تتبع git |

### النشر والتنظيف
| أمر | الوظيفة |
|---|---|
| `sudo bash az.sh deploy` | نشر كامل للإنتاج (nginx + systemd + venv) |
| `az.sh clean` | حذف `__pycache__`/`.pyc`/`.rasa` |

---

## 🔧 كيف يعمل `az.sh` تحت الغطاء

**1) تثبيت الحزم — مرحلتان لتجنّب `resolution-too-deep`:**
```
requirements/01-rasa.txt   → rasa-pro + rasa-sdk (يُثبَّت أولاً، يحسم numpy/scipy/pydantic إلخ)
requirements/02-extra.txt  → fastapi extras, openai, supabase, redis, bcrypt...
```
لو شغّلت `pip install -r requirements.txt` مباشرة، رايح تواجه نفس خطأ resolver القديم — استخدم `az.sh setup` أو `az.sh install` فقط.

**2) اختيار uv أو pip تلقائياً:**
- لو `uv` مثبَّت → يُستخدم (تثبيت أسرع بعشرات المرات، وresolver أقوى مع rasa-pro)
- لو غير مثبَّت → fallback كامل لـ `python3 -m venv` + `pip`
- تثبيت uv (اختياري لكن موصى به): `curl -LsSf https://astral.sh/uv/install.sh | sh`

**3) كشف بيئة الإنتاج تلقائياً:**
- لو وُجدت وحدة `systemd` بـ `azabot-webhook.service` → `on/off/restart/status/logs` تستخدم `systemctl`/`journalctl`
- غير ذلك (تطوير محلي/WSL) → يدير العمليات مباشرة عبر PID files في `.runtime/pids/`

**4) حماية التدريب من الإنتاج:**
`az.sh train` يستدعي `scripts/train-prod.sh` داخلياً، والذي يرفض التشغيل كلياً لو `NODE_ENV=production` إلا بتمرير `--force` صريح.

---

## 🗂️ بنية المشروع المرتبطة بـ az.sh

```
az.sh                       ← نقطة الدخول الوحيدة
requirements/
  01-rasa.txt                ← المرحلة 1: rasa-pro
  02-extra.txt                ← المرحلة 2: باقي الحزم
scripts/
  train-prod.sh                ← حارس التدريب (يستدعيه az.sh train)
  prod-check.sh                 ← فحص الجاهزية (يستدعيه az.sh check)
  gen_password_hash.py           ← توليد bcrypt (يستدعيه az.sh passwd)
  git-untrack-secrets.sh          ← تنظيف git (يستدعيه az.sh untrack)
deploy/production/
  deploy-production.sh             ← النشر الكامل (يستدعيه az.sh deploy)
.runtime/pids/                     ← PID files للعمليات المحلية
logs/                               ← لوجز كل خدمة (محلياً)
```

---

## 🆘 استكشاف الأخطاء الشائعة

```bash
# خطأ resolution-too-deep عند التثبيت
bash az.sh setup     # ← يثبّت بمرحلتين تلقائياً، يحل المشكلة

# بورت مشغول / عملية عالقة
bash az.sh heal

# نسيت كلمة مرور الأدمن
bash az.sh passwd

# السيرفر بطيء أو لا يستجيب
bash az.sh status
bash az.sh logs webhook

# عايز تدرّب موديل جديد وتنشره
NODE_ENV=dev bash az.sh release
scp models/alazab-*.tar.gz user@server:/opt/azabot/models/
ssh user@server "sudo systemctl restart azabot-rasa"
```
