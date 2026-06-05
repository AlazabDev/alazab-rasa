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
    "company_name", "brand_project_id", "identity_type", "brand_budget"
]

actions_to_add = [
    "action_create_brand_identity_request", "action_get_brand_project_status"
]

responses_to_add = {
    "utter_ask_company_name": [{"text": "ما هو اسم الشركة أو النشاط التجاري؟"}],
    "utter_ask_brand_project_id": [{"text": "برجاء إدخال رقم مشروع العلامة التجارية للتتبع:"}],
    "utter_ask_identity_type": [{"text": "ما هو نوع الهوية المطلوب (بصري، شعار فقط، متكامل)؟"}],
    "utter_ask_brand_budget": [{"text": "ما هي الميزانية المحددة لهذا المشروع؟"}],
    "utter_brand_request_created": [{"text": "تم استلام طلب الهوية التجارية بنجاح."}]
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
