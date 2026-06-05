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
    "supply_id", "material_type", "quantity", "delivery_date"
]

actions_to_add = [
    "action_create_supply_request", "action_get_supply_status"
]

responses_to_add = {
    "utter_brand_status": [{"text": "حالة المشروع الحالي: قيد التنفيذ."}],
    "utter_ask_supply_id": [{"text": "برجاء إدخال رقم طلب التوريد:"}],
    "utter_ask_material_type": [{"text": "ما هو نوع المواد المطلوب توريدها؟"}],
    "utter_ask_quantity": [{"text": "ما هي الكمية المطلوبة؟"}],
    "utter_ask_delivery_date": [{"text": "متى موعد التسليم المتوقع؟"}],
    "utter_supply_request_created": [{"text": "تم استلام طلب التوريد بنجاح."}],
    "utter_supply_status": [{"text": "حالة طلب التوريد الخاص بك: جاري التجهيز."}]
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
