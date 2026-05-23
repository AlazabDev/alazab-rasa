# AzaBot — تشخيص المعمارية والتصميم الصحيح
## Architecture Diagnosis & Correct Design

---

## المشكلة التي رصدتها

### الفكرة التي قلتها بالضبط:
```
الكيان واحد  ←  الشركة / القاعدة / الخدمات / الإدارة
التفرع يبدأ من  ←  شريحة العملاء وسياقهم
```

### المشكلة في التطبيق الحالي:

**1. domain.yml واحد يحمل كل شيء**
```
62 intent في ملف واحد — كل البراندات مخلوطة
- ask_alazab_quote
- ask_uberfix_request  
- ask_laban_bulk_order
- ask_luxury_materials
← CALM يحاول يفهم الكل في نفس الوقت
← كل طلب جديد يُعرَّض على كل الـ 62 intent
```

**2. collect_lead flow واحد مشترك لكل شرائح العملاء**
```
UberFix client  →  يمر بـ collect_lead العام
Laban client    →  يمر بـ collect_lead العام  
Alazab client   →  يمر بـ collect_lead العام
← نفس السؤال، نفس الـ slot، نفس المسار
← لكن احتياجات كل شريحة مختلفة تماماً
```

**3. context_memory slot مشترك**
```
- تُخزّن GPT context لكل محادثة
- لكن GPT prompt لا يعرف أي brand context هو فيه
- يستخرج نفس الحقول لـ UberFix client وـ CEO يسأل عن استثمار
```

**4. actions تقرأ slot "brand" من السياق لكن لا تضبطه مبكراً**
```
action_submit_lead يحاول يكتشف البراند من intent_map آخر المحادثة
← fragile — إذا ما ذُكر intent البراند مش هيعرف
```

---

## القاعدة الصحيحة

```
الكيان الواحد (الشركة) = Core Layer:
  - قاعدة البيانات المشتركة
  - خدمات الإشعارات (WhatsApp, Telegram)
  - GPT client المشترك
  - Knowledge base مشترك
  - Human handoff مشترك

التفرع عند = Customer Segment Context:
  - Brand identifier (يُضبط من أول رسالة)
  - NLU scope (كل brand يرى intents خاصة به فقط)
  - Flow مخصص (مسار العميل بحسب شريحته)
  - Slot context مخصص (بيانات كل شريحة مختلفة)
  - Response personality مخصص (نبرة كل brand)
```

---

## المعمارية الصحيحة

```
┌─────────────────────────────────────────────────────────┐
│                    CORE (مشترك)                          │
│  DB · GPT · WhatsApp · Notifications · Knowledge        │
│  Human Handoff · Feedback · Session Management          │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │ SEGMENT │   │ SEGMENT │   │ SEGMENT │
   │UberFix  │   │ Laban   │   │Alazab/  │
   │B2C      │   │B2B      │   │Luxury/  │
   │صيانة    │   │توريدات  │   │Brand    │
   └────┬────┘   └────┬────┘   └────┬────┘
        │              │              │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │ NLU     │   │ NLU     │   │ NLU     │
   │ Scope   │   │ Scope   │   │ Scope   │
   │ خاص     │   │ خاص     │   │ خاص     │
   └────┬────┘   └────┬────┘   └────┬────┘
        │              │              │
   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
   │ Flows   │   │ Flows   │   │ Flows   │
   │ مسارات  │   │ مسارات  │   │ مسارات  │
   │ خاصة    │   │ خاصة    │   │ خاصة    │
   └─────────┘   └─────────┘   └─────────┘
```

---

## القواعد الثلاث التي تمنع تشتت الوكلاء

### القاعدة 1: Brand Context أول خطوة
```yaml
# كل entry point في الـ webhook يضبط brand slot أولاً
# قبل أي flow يبدأ

# في rasa_client.py:
payload = {
  "sender": sender_id,
  "message": text,
  "metadata": {
    "brand": resolved_brand,  # يُضبط من الـ URL / domain
    "channel": channel,
  }
}

# في domain.yml:
slots:
  brand:
    type: categorical
    values:
      - uberfix
      - laban_alasfour  
      - alazab_construction
      - luxury_finishing
      - brand_identity
    mappings:
      - type: from_trigger_intent  # يُضبط من metadata
        intent: session_start
        value: metadata.brand
```

### القاعدة 2: كل Segment له NLU scope خاص
```
# بدلاً من 62 intent مخلوطة:

data/segments/
  uberfix/
    nlu.yml      ← 8 intents فقط خاصة بـ UberFix
    flows.yml    ← مسارات الصيانة
    domain.yml   ← slots + responses خاصة
  laban/
    nlu.yml      ← 6 intents فقط خاصة بـ Laban
    flows.yml    ← مسار طلب التصنيع
    domain.yml   ← slots + responses خاصة
  construction/
    nlu.yml      ← intents خاصة
    flows.yml
    domain.yml
  
core/
  nlu.yml       ← intents مشتركة: greet, bye, help, handoff
  flows.yml     ← flows مشتركة: collect_lead, human_handoff, feedback
  domain.yml    ← slots + responses مشتركة
```

### القاعدة 3: collect_lead يعكس سياق الـ Segment
```yaml
# ❌ الحالي — collect_lead عام لا يعرف السياق:
collect_lead:
  steps:
    - collect: user_name
    - collect: user_phone
    - collect: user_message
    - action: action_submit_lead

# ✅ الصحيح — كل segment له collect flow خاص أو branch:
collect_lead:
  steps:
    - action: action_accumulate_context  # يعرف البراند من slot
    - collect: user_name
    - collect: user_phone
    - id: branch_by_brand
      action: action_noop
      next:
        - if: slots.brand = "uberfix"
          then: collect_uberfix_details
        - if: slots.brand = "laban_alasfour"
          then: collect_laban_details
        - else: collect_general_details
    - id: collect_uberfix_details
      collect: service_type        # فقط لـ UberFix
    - id: collect_laban_details
      collect: unit_type           # فقط لـ Laban
      collect: material_type       # فقط لـ Laban
    - id: collect_general_details
      collect: user_message
    - action: action_submit_lead
```

---

## الخريطة الجديدة المقترحة

```
alazab-rasa/
├── data/
│   ├── core/                    ← مشترك بين كل الـ segments
│   │   ├── nlu.yml             ← greet, bye, help, handoff, bot_challenge
│   │   ├── flows.yml           ← hello, goodbye, human_handoff, feedback
│   │   └── collect_lead.yml    ← collect_lead (مع branching)
│   │
│   └── segments/               ← كل segment معزول
│       ├── uberfix/
│       │   ├── nlu.yml         ← intents الصيانة فقط
│       │   ├── flows.yml       ← uberfix_request, track, subscribe
│       │   └── responses.yml   ← ردود UberFix فقط
│       ├── laban/
│       │   ├── nlu.yml         ← intents التوريد والتصنيع
│       │   ├── flows.yml       ← laban_inquiry → redirect_to_site
│       │   └── responses.yml
│       ├── construction/
│       │   ├── nlu.yml
│       │   ├── flows.yml
│       │   └── responses.yml
│       ├── luxury/
│       │   ├── nlu.yml
│       │   ├── flows.yml
│       │   └── responses.yml
│       └── brand_identity/
│           ├── nlu.yml
│           ├── flows.yml
│           └── responses.yml
│
├── domain/
│   ├── core.yml               ← slots + actions المشتركة
│   └── segments/
│       ├── uberfix.yml        ← slots + actions خاصة بـ UberFix
│       ├── laban.yml
│       ├── construction.yml
│       ├── luxury.yml
│       └── brand_identity.yml
│
└── actions/
    ├── core/                  ← db, gpt, whatsapp (موجودة)
    ├── segment_uberfix/       ← actions UberFix فقط
    ├── segment_laban/         ← actions Laban فقط
    └── segment_shared/        ← shared actions (submit_lead, handoff)
```

---

## تدفق عمل UberFix بشكل صحيح

```
1. المستخدم يفتح uberfix.alazab.com
   → webhook يضبط metadata.brand = "uberfix"
   → Rasa يضبط slot brand = "uberfix" من session_start

2. المستخدم يكتب "السباكة عطلانة"
   → CALM يبحث في NLU scope الخاص بـ UberFix فقط
   → intent: ask_uberfix_request (ثقة عالية لأن scope محدود)
   → يبدأ flow: uberfix_request

3. uberfix_request flow:
   → action_accumulate_context (يعرف brand=uberfix)
   → GPT prompt يعرف: "أنت محلل طلبات صيانة UberFix"
   → يجمع: موقع، نوع عطل، أولوية
   → لا يسأل عن نوع نشاط أو هوية تجارية (لأن scope محدد)

4. action_submit_lead:
   → brand = "uberfix" (من slot)
   → يُرسل لـ webhook /lead بشكل صحيح
   → يُنشئ طلب في UberFix DB
```

---

## تدفق عمل Laban بشكل صحيح

```
1. المستخدم يسأل في أي قناة عن وحدات خشبية/تصاميم
   → intent: ask_laban_woodwork (أو ask_laban_products)
   → CALM يشغّل flow: laban_inquiry

2. laban_inquiry flow:
   steps:
     - action: utter_laban_redirect  
       # "لمعرفة تفاصيل الوحدات وتجربة التصاميم
       #  زور موقعنا المتخصص:"
       # "🪵 laban-alasfour.alazab.com"
     - action: utter_laban_cta
       # "أو اترك بياناتك وفريقنا يتواصل معاك"
     - link: collect_lead  # مع brand="laban_alasfour"

3. في لوحة الأدمن:
   → طلب يظهر في Laban Orders
   → الفريق يتابع من الواجهة التي بنيناها
```

---

## الخلاصة العملية (ماذا نفعل الآن)

### أولوية 1 — فوري (لا يحتاج re-train)
- ✅ ضبط `brand` slot من metadata في كل دخول
- ✅ كل segment action تتحقق من `brand` قبل التنفيذ
- ✅ `collect_lead` يأخذ `brand` من slot وليس من intent detection

### أولوية 2 — قصير المدى (إعادة تنظيم الملفات)
- فصل domain.yml إلى core + segments
- تقليص الـ intents في كل scope
- collect_lead branching بحسب brand

### أولوية 3 — متوسط المدى (GPT Context Awareness)
- EXTRACTION_PROMPT في action_context_accumulator
  يعرف الـ brand ويستخرج الحقول المناسبة لكل segment
- لا تسأل UberFix client عن "نوع الشعار"
- لا تسأل Laban client عن "مساحة الوحدة بالمتر"
