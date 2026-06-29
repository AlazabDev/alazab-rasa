import yaml
from pathlib import Path

ROOT = Path('/home/azab/prod/alazab-rasa-prod')
domain_file = ROOT / 'domain.yml'
general_file = ROOT / 'domain/general.yml'

with open(domain_file, 'r', encoding='utf-8') as f:
    domain_data = yaml.safe_load(f)

includes = domain_data.get('includes', [])

with open(general_file, 'r', encoding='utf-8') as f:
    general_data = yaml.safe_load(f)

# Collect all slots and responses from other included files
all_other_slots = set()
all_other_responses = set()

for inc in includes:
    if inc == 'domain/general.yml':
        continue
    inc_path = ROOT / inc
    if not inc_path.exists():
        continue
    with open(inc_path, 'r', encoding='utf-8') as f:
        inc_data = yaml.safe_load(f) or {}
    
    if 'slots' in inc_data:
        all_other_slots.update(inc_data['slots'].keys())
    if 'responses' in inc_data:
        all_other_responses.update(inc_data['responses'].keys())

if 'slots' in general_data:
    for slot in list(general_data['slots'].keys()):
        if slot in all_other_slots:
            print(f"Removing duplicate slot from general.yml: {slot}")
            del general_data['slots'][slot]

if 'responses' in general_data:
    for resp in list(general_data['responses'].keys()):
        if resp in all_other_responses:
            print(f"Removing duplicate response from general.yml: {resp}")
            del general_data['responses'][resp]

with open(general_file, 'w', encoding='utf-8') as f:
    yaml.safe_dump(general_data, f, allow_unicode=True, sort_keys=False, width=1000)

print("Fixed duplicates in domain/general.yml")
