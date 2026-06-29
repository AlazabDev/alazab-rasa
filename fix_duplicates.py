import yaml
from pathlib import Path

ROOT = Path('/home/azab/prod/alazab-rasa-prod')
domain_file = ROOT / 'domain.yml'

with open(domain_file, 'r', encoding='utf-8') as f:
    domain_data = yaml.safe_load(f)

includes = domain_data.get('includes', [])

for inc in includes:
    inc_path = ROOT / inc
    if not inc_path.exists():
        continue
    with open(inc_path, 'r', encoding='utf-8') as f:
        inc_data = yaml.safe_load(f) or {}
    
    # Remove duplicate slots
    if 'slots' in inc_data and 'slots' in domain_data:
        for slot in inc_data['slots']:
            if slot in domain_data['slots']:
                print(f"Removing duplicate slot: {slot}")
                del domain_data['slots'][slot]
                
    # Remove duplicate responses
    if 'responses' in inc_data and 'responses' in domain_data:
        for resp in inc_data['responses']:
            if resp in domain_data['responses']:
                print(f"Removing duplicate response: {resp}")
                del domain_data['responses'][resp]

with open(domain_file, 'w', encoding='utf-8') as f:
    yaml.safe_dump(domain_data, f, allow_unicode=True, sort_keys=False, width=1000)

print("Fixed duplicates in domain.yml")
