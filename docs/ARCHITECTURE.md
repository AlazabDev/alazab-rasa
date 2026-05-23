# AzaBot — تقرير إعادة الهيكلة v4.0
## Architecture Refactoring Report

---

## الوضع السابق vs الحالي

| الملف | قبل | بعد |
|-------|-----|-----|
| `webhook/server.py` | **3649 سطر** ← كل شيء مدفون | **268 سطر** ← app + health + startup |
| `webhook/routers/admin.py` | — (مدفون في server.py) | ✅ **مستقل** — /admin/* |
| `webhook/routers/chat.py` | — (مدفون في server.py) | ✅ **مستقل** — /chat/* |
| `webhook/routers/channels.py` | — (مدفون في server.py) | ✅ **مستقل** — /webhook/*, /brands |
| `webhook/services/integrations.py` | — (مدفون في server.py) | ✅ **مستقل** — محرك التكاملات |
| `webhook/_uberfix_gateway.py` | — (مدفون في server.py) | ✅ **مستقل** — UberFix DB engine |
| `actions/core/db.py` | — | ✅ **جديد** — Connection Pool |
| `actions/core/gpt.py` | — | ✅ **جديد** — GPT client مع cache |
| `actions/core/whatsapp.py` | — | ✅ **جديد** — مُرسِل موحد |
| `actions/action_general.py` | aiohttp + raw db | ✅ استخدام core layer |
| `actions/action_context_accumulator.py` | raw HTTP GPT | ✅ استخدام core.gpt |
| `actions/action_human_handoff.py` | openai مباشر | ✅ استخدام core.gpt |
| `actions/action_submit_lead.py` | كود WhatsApp مكرر | ✅ استخدام core.whatsapp |
| `actions/knowledge_search.py` | Instance جديد كل طلب | ✅ Singleton Pattern |

---

## البنية الجديدة الكاملة

```
alazab-rasa/
├── actions/
│   ├── core/                    ← [جديد] الطبقة المشتركة
│   │   ├── __init__.py
│   │   ├── db.py               ← asyncpg Connection Pool
│   │   ├── gpt.py              ← GPT client (cache + rate limit + retry)
│   │   └── whatsapp.py         ← مُرسِل WhatsApp موحد
│   │
│   ├── maintenance/             ← طبقة UberFix (نظيفة مسبقاً)
│   │   ├── errors.py
│   │   ├── gateway_client.py
│   │   ├── responses.py
│   │   ├── schemas.py
│   │   └── service.py
│   │
│   ├── brand_actions/           ← أوامر البراندات
│   │   ├── alazab_construction.py
│   │   ├── brand_identity.py
│   │   ├── laban_alasfour.py
│   │   ├── luxury_finishing.py
│   │   └── uberfix.py
│   │
│   ├── config.py               ← إعدادات مركزية
│   ├── knowledge_search.py     ← [محسّن] Singleton + Arabic normalization
│   ├── form_validation.py
│   ├── action_brand_navigator.py
│   ├── action_context_accumulator.py  ← [محسّن] → core.gpt
│   ├── action_daftra_ops.py
│   ├── action_general.py              ← [محسّن] → core layer
│   ├── action_human_handoff.py        ← [محسّن] → core.gpt + core.whatsapp
│   ├── action_send_sweets_info.py
│   ├── action_submit_lead.py          ← [محسّن] → core.whatsapp
│   ├── action_uberfix_ops.py
│   └── whatsapp_sender.py            ← (legacy — Supabase templates)
│
└── webhook/
    ├── server.py               ← [268 سطر] app + middleware + health
    ├── config.py               ← إعدادات مركزية
    ├── middleware.py           ← SecurityHeadersMiddleware
    ├── models.py               ← Pydantic models
    ├── utils.py                ← دوال مساعدة مشتركة
    ├── _uberfix_gateway.py     ← [مُستخرَج] UberFix DB engine
    │
    ├── routers/                ← [جديد] FastAPI Routers
    │   ├── __init__.py
    │   ├── admin.py            ← /admin/* (login, stats, API)
    │   ├── chat.py             ← /chat, /chat/upload, /chat/audio, /chat/tts
    │   └── channels.py        ← /webhook/meta, /webhook/telegram, /brands, /lead
    │
    └── services/               ← طبقة الخدمات
        ├── __init__.py
        ├── admin_data.py       ← CRUD لوحة التحكم (JSON storage)
        ├── audio.py            ← Transcription + TTS (OpenAI)
        ├── channels.py         ← [محسّن] إرسال موحد
        ├── integrations.py     ← [جديد] محرك التكاملات (7 أنواع)
        ├── notifications.py    ← إشعارات leads
        ├── rasa_client.py      ← HTTP client لـ Rasa Pro
        └── uploads.py          ← رفع الملفات
```

---

## المشاكل التي حُلّت

### 1. التكرار (DRY violations)
- ✅ `_send_whatsapp` كانت مكتوبة في **3 ملفات** → الآن `actions/core/whatsapp.py` واحد
- ✅ `_load_admin_data` / `_save_admin_data` كانتا في `server.py` رغم وجودهما في `admin_data.py`
- ✅ `_rasa_send` كانت في `server.py` رغم `rasa_client.py`

### 2. الـ God File
- ✅ `server.py`: 3649 → 268 سطر (92% تخفيض)
- ✅ integration engine مستقل في `services/integrations.py`
- ✅ admin router مستقل في `routers/admin.py`
- ✅ UberFix gateway مستقل في `_uberfix_gateway.py`

### 3. أداء الباك-إند
- ✅ **DB Connection Pool** — بدلاً من فتح connection جديد لكل action
- ✅ **GPT Cache** (256 نتيجة) — توفير OpenAI tokens
- ✅ **GPT Semaphore** (max 5) — منع rate limit flood
- ✅ **KnowledgeSearch Singleton** — قراءة JSON مرة واحدة فقط

### 4. معمارية Actions
- ✅ كل action تستخدم `core` layer — لا استدعاء API مباشر
- ✅ `action_submit_lead.py` → webhook + WhatsApp fallback pattern صحيح

### 5. Admin API
- ✅ من `if/elif` chain بلا نهاية → `dispatch table` (dict of handlers)
- ✅ كل action في دالة معزولة مستقلة
- ✅ Rate limiting محسّن مع config من .env

---

## الملفات التي لم تتغير (لا تحتاج تعديل)
- `actions/maintenance/*` — طبقة UberFix نظيفة مسبقاً
- `actions/brand_actions/*` — خفيفة ونظيفة
- `webhook/utils.py` — دوال مساعدة سليمة
- `webhook/middleware.py` — Security headers
- `webhook/models.py` — Pydantic models صحيحة
- `webhook/services/rasa_client.py` — نظيف
- `webhook/services/uploads.py` — نظيف
- `webhook/services/audio.py` — نظيف

---

## خطوات التطبيق (بدون downtime)

```bash
# 1. تأكد من requirements
pip install asyncpg httpx psutil --break-system-packages

# 2. اختبر imports
python -c "from webhook.server import app; print('OK')"
python -c "from actions.core import insert, send_whatsapp, gpt_complete; print('OK')"

# 3. أعد تشغيل الـ webhook server
systemctl restart azabot-webhook

# 4. أعد تشغيل الـ actions server  
systemctl restart azabot-actions
```

---

## متغيرات .env الجديدة (اختيارية)

```env
# GPT Rate Control
GPT_MAX_CONCURRENT=5
GPT_TIMEOUT_SECONDS=30

# Channel Send Timeout
CHANNEL_SEND_TIMEOUT=10

# Admin Rate Limit
ADMIN_LOGIN_MAX_ATTEMPTS=10
ADMIN_LOGIN_WINDOW_SECONDS=300
```
