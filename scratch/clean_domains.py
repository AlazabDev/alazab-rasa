import yaml
import sys
import os

path = '/home/azab/azabot/alazab-rasa/domain/general.yml'

def clean_domain(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    if not data:
        return
    
    if 'actions' in data and isinstance(data['actions'], list):
        # Remove utter_ responses from actions list
        data['actions'] = [a for a in data['actions'] if not a.startswith('utter_')]
    
    # Also fix from_llm to custom if any
    if 'slots' in data:
        for slot_name, slot_data in data['slots'].items():
            if 'mappings' in slot_data:
                for mapping in slot_data['mappings']:
                    if mapping.get('type') == 'from_llm':
                        mapping['type'] = 'custom'

    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)

clean_domain(path)
# Also clean other domain files
domain_files = [
    'domain/alazab.yml',
    'domain/luxury_finishing.yml',
    'domain/brand_identity.yml',
    'domain/laban_alasfour.yml',
    'domain/uberfix.yml',
    'domain.yml'
]
for f in domain_files:
    clean_domain(os.path.join('/home/azab/azabot/alazab-rasa', f))
