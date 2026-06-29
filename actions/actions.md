# 📂 `actions/` — دليل الـ Actions الكاملة

## الهيكل العام

```
actions/
├── config.py                          # الإعدادات المركزية (env vars)
├── action_brand_navigator.py          # action_brand_navigator
├── action_context_accumulator.py      # action_accumulate_context, action_smart_slot_check,
│                                      # action_confirm_understanding, action_build_full_request
├── action_create_maintenance_request.py  # (legacy shim — فارغ، الـ action في brand_actions/uberfix.py)
├── action_daftra_ops.py               # action_daftra_sync_client, action_daftra_create_invoice
├── action_general.py                  # action_save_lead_to_crm, action_notify_sales_team,
│                                      # action_receive_handoff_reason, action_check_human_availability,
│                                      # action_check_queue_position, action_initiate_human_handoff,
│                                      # action_wait_for_agent, action_transfer_to_agent,
│                                      # action_notify_team_via_whatsapp,
│                                      # action_collect_escalation_details, action_create_escalation_ticket,
│                                      # action_create_project, action_notify_manager,
│                                      # action_receive_feedback_service, action_receive_rating,
│                                      # action_receive_feedback_text, action_receive_suggestion,
│                                      # action_save_feedback, action_save_suggestion,
│                                      # action_collect_follow_up_contact,
│                                      # action_search_faq_by_keyword
├── action_human_handoff.py            # action_human_handoff (GPT summary + WhatsApp notify)
├── action_send_sweets_info.py         # action_send_sweets_info (placeholder)
├── action_submit_lead.py              # action_submit_lead
├── action_uberfix_ops.py              # action_uberfix_triage_request
├── form_validation.py                 # validate_collect_lead_form, validate_maintenance_form
├── knowledge_search.py                # KnowledgeSearch (helper class, not a Rasa action)
├── whatsapp_sender.py                 # WhatsApp template sender (helper module)
│
├── brand_actions/
│   ├── alazab_construction.py         # action_alazab_get_quote, action_alazab_show_projects
│   ├── brand_identity.py              # action_brand_get_quote, action_brand_show_process,
│   │                                  # action_brand_show_industries
│   ├── laban_alasfour.py              # action_laban_show_catalog, action_laban_bulk_quote,
│   │                                  # action_laban_check_delivery
│   ├── luxury_finishing.py            # action_luxury_get_quote, action_luxury_show_materials
│   └── uberfix.py                     # action_uberfix_create_request ✅ (الـ action الرئيسي)
│                                      # action_uberfix_track_request ✅
│                                      # action_uberfix_show_subscriptions ✅
│
└── maintenance/                       # طبقة الخدمة المعزولة (لا تحتوي Rasa actions مباشرة)
    ├── errors.py                      # MaintenanceValidationError, MaintenanceConfigError, MaintenanceGatewayError
    ├── gateway_client.py              # MaintenanceGatewayClient (يدعم maintenance-gateway + bot-gateway)
    ├── responses.py                   # ردود المستخدم الجاهزة
    ├── schemas.py                     # MaintenanceRequest, MaintenanceTicket, build_create_request
    └── service.py                     # MaintenanceService (create_request, track_request, subscriptions)
```

---

## متغيرات البيئة المطلوبة

| المتغير | الاستخدام |
|---------|-----------|
| `MAINTENANCE_GATEWAY_URL` | بوابة الصيانة (maintenance-gateway) |
| `UBERFIX_BOT_GATEWAY_URL` | بوابة البوت (bot-gateway) — الأولوية |
| `MAINTENANCE_API_KEY` أو `UBERFIX_API_KEY` | مفتاح API للبوابة |
| `UBERFIX_STATUS_API_URL` | API استعلام الحالة (اختياري) |
| `UBERFIX_TRACK_BASE_URL` | رابط تتبع الطلب (افتراضي: https://uberfix.shop/track) |
| `OPENAI_API_KEY` | لـ action_accumulate_context و action_human_handoff |
| `OPENAI_HANDOFF_MODEL` | نموذج GPT للتلخيص (افتراضي: gpt-4o-mini) |
| `WHATSAPP_API_URL` | Meta WhatsApp Cloud API URL |
| `WHATSAPP_TOKEN` أو `META_TOKEN` | توكن WhatsApp |
| `NOTIFY_PHONE` | رقم هاتف فريق الدعم للإشعارات |
| `DAFTRA_SUBDOMAIN` | نطاق دفترة (مثال: alazab) |
| `DAFTRA_API_KEY` | مفتاح API دفترة |
| `DB_HOST/PORT/NAME/USER/PASSWORD` | PostgreSQL للـ CRM والـ leads |
| `SUPABASE_URL` + `SUPABASE_API_KEY` | لـ whatsapp_sender (قوالب WhatsApp) |

---

## ملاحظات مهمة

- **`action_uberfix_create_request`** و **`action_uberfix_track_request`** موجودان في `brand_actions/uberfix.py` فقط.
  لا تُعرّفهما في أي ملف آخر لتجنب تعارض الأسماء.

- **`action_create_maintenance_request.py`** فارغ عمداً (legacy shim).

- **`maintenance/`** هي طبقة خدمة نظيفة — لا تستورد منها مباشرة إلا عبر `MaintenanceService`.

- **`whatsapp_sender.py`** و **`knowledge_search.py`** مكتبات مساعدة وليست Rasa actions.
