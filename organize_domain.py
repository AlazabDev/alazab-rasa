import yaml
from pathlib import Path

ROOT = Path('/home/azab/prod/alazab-rasa-prod')
domain_file = ROOT / 'domain.yml'
general_file = ROOT / 'domain/general.yml'
maintenance_file = ROOT / 'domain/general/maintenance.yml'
brands_file = ROOT / 'domain/brands/alazab_group.yml'

# Ensure directories exist
brands_file.parent.mkdir(parents=True, exist_ok=True)

with open(general_file, 'r', encoding='utf-8') as f:
    general_data = yaml.safe_load(f)

with open(maintenance_file, 'r', encoding='utf-8') as f:
    maintenance_data = yaml.safe_load(f)

if brands_file.exists():
    with open(brands_file, 'r', encoding='utf-8') as f:
        brands_data = yaml.safe_load(f) or {}
else:
    brands_data = {"version": "3.1", "responses": {}}

maintenance_responses = ['utter_maintenance_fast_start', 'utter_ask_branch_name', 'utter_ask_service_item']
brand_responses = ['utter_alazab_about', 'utter_brand_services', 'utter_luxury_services', 'utter_laban_products']

responses = general_data.get('responses', {})

# Move to maintenance
if 'responses' not in maintenance_data:
    maintenance_data['responses'] = {}
for r in maintenance_responses:
    if r in responses:
        maintenance_data['responses'][r] = responses[r]
        del general_data['responses'][r]

# Move to brands
if 'responses' not in brands_data:
    brands_data['responses'] = {}
for r in brand_responses:
    if r in responses:
        brands_data['responses'][r] = responses[r]
        del general_data['responses'][r]

# Write back
with open(general_file, 'w', encoding='utf-8') as f:
    yaml.safe_dump(general_data, f, allow_unicode=True, sort_keys=False, width=1000)

with open(maintenance_file, 'w', encoding='utf-8') as f:
    yaml.safe_dump(maintenance_data, f, allow_unicode=True, sort_keys=False, width=1000)

with open(brands_file, 'w', encoding='utf-8') as f:
    yaml.safe_dump(brands_data, f, allow_unicode=True, sort_keys=False, width=1000)

# Update domain.yml includes
with open(domain_file, 'r', encoding='utf-8') as f:
    domain_data = yaml.safe_load(f)

includes = domain_data.get('includes', [])
if 'domain/brands/alazab_group.yml' not in includes:
    includes.append('domain/brands/alazab_group.yml')
domain_data['includes'] = includes

with open(domain_file, 'w', encoding='utf-8') as f:
    yaml.safe_dump(domain_data, f, allow_unicode=True, sort_keys=False, width=1000)

print("Files successfully reorganized!")
