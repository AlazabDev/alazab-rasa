# دليل Git — AzaBot مع GitHub
## github.com/AlazabDev/alazab-rasa

---

## الوضع الحالي على السيرفر

```
~/azabot/alazab-rasa/   ← المشروع الحالي (مع .git)
Remote: AlazabDev/alazab-rasa
Branch: main
```

---

## الخطوة 1 — تحضير GitHub Token

على GitHub:
`Settings → Developer Settings → Personal Access Tokens → Tokens (classic)`

صلاحيات مطلوبة: `repo` (كاملة)

```bash
# احفظ الـ token
export GITHUB_TOKEN=ghp_your_token_here
# أو في .env (لا يُرفع على git)
echo "GITHUB_TOKEN=ghp_your_token" >> ~/.env_local
```

---

## الخطوة 2 — ضبط git config (مرة واحدة)

```bash
cd ~/azabot/alazab-rasa

# هوية المطوّر
git config user.email "devops@alazab.com"
git config user.name "AzaBot DevOps"

# credential helper (يحفظ الـ token)
git config credential.helper store

# تحقق من الـ remote
git remote -v
# يجب أن يظهر:
# origin  https://github.com/AlazabDev/alazab-rasa.git (fetch)
# origin  https://github.com/AlazabDev/alazab-rasa.git (push)
```

إذا لم يكن الـ remote مضبوطاً:
```bash
git remote add origin https://github.com/AlazabDev/alazab-rasa.git
# أو
git remote set-url origin https://github.com/AlazabDev/alazab-rasa.git
```

---

## الخطوة 3 — رفع التغييرات الحالية

```bash
cd ~/azabot/alazab-rasa

# استخدم السكريبت المدمج
bash scripts/git-sync.sh push
```

أو يدوياً:
```bash
# فحص ما تغيّر
git status

# إضافة الملفات المحددة (الأكثر أماناً)
git add actions/ data/ domain/ domain.yml
git add webhook/ deploy/ scripts/
git add piper/pronunciation_lexicon.yml piper/voices.json
git add piper/generate_brand_samples.py piper/configs/
git add piper/sentences/ piper/voice/code/
git add config.yml pyproject.toml requirements.txt
git add .gitignore .env.example Makefile README.md
git add wsl-setup.sh wsl-test.sh run.sh dev.sh

# ⚠️ تحقق قبل الـ commit
git diff --cached --name-only

# commit
git commit -m "feat: AzaBot v4.0 — full refactor + deploy configs"

# push
git push origin main
```

---

## الخطوة 4 — سحب التغييرات من GitHub (Pull)

```bash
bash scripts/git-sync.sh pull
# أو
git pull origin main
```

---

## قواعد ذهبية لا تخترق

```bash
# ❌ لا تفعل أبداً
git add .                    # يضيف كل شيء بما فيه .env
git add -A                   # نفس المشكلة
git add .env                 # secrets!
git add azabot/.env          # secrets!
git add RASA_LICENSE*        # license key!
git add piper/*.onnx         # ملفات ضخمة ~63MB لكل واحد

# ✅ افعل
git add <ملف محدد>           # دائماً حدد الملف
git status                   # تحقق قبل كل commit
git diff --cached            # راجع ما ستُرفعه
bash scripts/git-sync.sh push  # استخدم السكريبت
```

---

## workflow الموصى به — يومياً

```bash
cd ~/azabot/alazab-rasa

# 1. سحب آخر التغييرات أولاً
bash scripts/git-sync.sh pull

# 2. تعديلاتك...

# 3. رفع تغييراتك
bash scripts/git-sync.sh push

# أو مع message مخصص
GIT_MSG="fix: Laban redirect flow" bash scripts/git-sync.sh push
```

---

## إذا رفض git push (Permission denied)

```bash
# 1. تحقق من الـ token
git ls-remote origin

# 2. استخدم HTTPS مع token مباشرة
git remote set-url origin \
  https://ghp_YOUR_TOKEN@github.com/AlazabDev/alazab-rasa.git

# 3. أو استخدم SSH
ssh-keygen -t ed25519 -C "devops@alazab.com"
cat ~/.ssh/id_ed25519.pub
# أضفها في GitHub → Settings → SSH Keys
git remote set-url origin git@github.com:AlazabDev/alazab-rasa.git
```

---

## ملفات محمية — موجودة في .gitignore

| الملف | السبب |
|-------|-------|
| `.env` | كلمات سر + API keys |
| `azabot/.env` | Supabase secrets |
| `RASA_LICENSE1/2/3` | License key مدفوع |
| `piper/*.onnx` | ~63MB لكل ملف |
| `piper/voice/audio/` | MP3/WAV recordings |
| `models/` | ملفات Rasa المدرّبة (كبيرة) |
| `.runtime/` | بيانات runtime |
| `logs/` | logs |

---

## تشغيل بعد pull

```bash
# إذا تغيّر requirements.txt
pip install -r requirements.txt

# إذا تغيّر domain.yml
python3 scripts/render_runtime_domain.py
python3 scripts/deep_clean.py --validate-only

# إذا تغيّرت actions أو data
bash scripts/botctl.sh train

# إعادة تشغيل
bash scripts/botctl.sh restart
```
