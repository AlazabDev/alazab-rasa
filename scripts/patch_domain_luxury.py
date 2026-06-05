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
    "finishing_type", "finishing_budget", "project_id", "customer_question"
]

actions_to_add = [
    "action_create_luxury_finishing_request", "action_get_luxury_project_status",
    "action_check_customer_query"
]

responses_to_add = {
    "utter_ask_finishing_type": [{"text": "ما هو نوع التشطيب المطلوب؟"}],
    "utter_ask_finishing_budget": [{"text": "ما هي الميزانية التقريبية؟"}],
    "utter_luxury_request_created": [{"text": "تم استلام طلب التشطيب الفاخر بنجاح."}],
    "utter_ask_project_id": [{"text": "برجاء إدخال معرف المشروع:"}],
    "utter_luxury_status": [{"text": "حالة مشروعك الحالي هي: قيد التنفيذ."}],
    "utter_ask_customer_question": [{"text": "كيف يمكنني مساعدتك اليوم؟"}],
    "utter_what_can_you_do": [{"text": "يمكنني مساعدتك في كافة خدمات مجموعة العزب."}]
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
