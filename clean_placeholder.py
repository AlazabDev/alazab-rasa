import yaml
from pathlib import Path

ROOT = Path('/home/azab/prod/alazab-rasa-prod')
placeholder_file = ROOT / 'domain/general/placeholder_domain.yml'

with open(placeholder_file, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

if 'responses' in data:
    for resp in ['utter_ask_rephrase', 'utter_placeholder']:
        if resp in data['responses']:
            del data['responses'][resp]

with open(placeholder_file, 'w', encoding='utf-8') as f:
    yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=1000)

print("Cleaned placeholder")
