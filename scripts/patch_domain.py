import yaml
import os

domain_path = "domain/general.yml"
with open(domain_path, "r", encoding="utf-8") as f:
    domain_data = yaml.safe_load(f)

if "slots" not in domain_data:
    domain_data["slots"] = {}
if "responses" not in domain_data:
    domain_data["responses"] = {}
if "actions" not in domain_data:
    domain_data["actions"] = []

# List of things to add
slots_to_add = [
    "client_name", "client_phone", "service_type", "description", 
    "priority", "request_number", "maintenance_request_id"
]

actions_to_add = [
    "action_create_maintenance_request", "action_get_maintenance_status",
    "action_triage_maintenance_request", "action_assign_maintenance_request"
]

responses_to_add = {
    "utter_ask_client_name": [{"text": "من فضلك أدخل اسم العميل:"}],
    "utter_ask_client_phone": [{"text": "ما هو رقم الهاتف للتواصل؟"}],
    "utter_ask_service_type": [{"text": "ما هو نوع الخدمة أو القسم؟"}],
    "utter_ask_description": [{"text": "يرجى وصف المشكلة بوضوح:"}],
    "utter_ask_priority": [{"text": "ما هي درجة الأهمية (عادي، طارئ)؟"}],
    "utter_ask_request_number": [{"text": "يرجى إدخال رقم طلب الصيانة للتتبع:"}],
    "utter_request_created": [{"text": "تم إنشاء طلب الصيانة بنجاح. سيتم التواصل معك قريباً."}],
    "utter_status": [{"text": "حالة الطلب الحالية هي: قيد المراجعة."}],
    "utter_maintenance_triaged": [{"text": "تم مراجعة الطلب فنياً."}],
    "utter_maintenance_assigned": [{"text": "تم تعيين الفني بنجاح."}],
    "utter_ask_maintenance_request_id": [{"text": "يرجى إدخال رقم الطلب الداخلي:"}]
}

for s in slots_to_add:
    if s not in domain_data["slots"]:
        domain_data["slots"][s] = {"type": "text", "mappings": [{"type": "custom"}]}

for a in actions_to_add:
    if a not in domain_data["actions"]:
        domain_data["actions"].append(a)

for r, val in responses_to_add.items():
    if r not in domain_data["responses"]:
        domain_data["responses"][r] = val

with open(domain_path, "w", encoding="utf-8") as f:
    yaml.safe_dump(domain_data, f, allow_unicode=True, sort_keys=False)

print("Domain patched successfully.")
