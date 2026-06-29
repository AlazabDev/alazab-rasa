import yaml
import os
import shutil
from pathlib import Path

ROOT = Path('/home/azab/prod/alazab-rasa-prod')
data_dir = ROOT / 'data'
general_dir = data_dir / 'general'
flows_dir = data_dir / 'flows'
rules_file = data_dir / 'rules' / 'rules.yml'

# 1. Delete dummy files
dummy_files = [general_dir / 'nlu.yml', general_dir / 'rules.yml']
for f in dummy_files:
    if f.exists():
        f.unlink()
        print(f"Deleted {f}")

# 2. Add nlu_trigger to feedback.yml if missing
feedback_file = general_dir / 'feedback.yml'
if feedback_file.exists():
    with open(feedback_file, 'r', encoding='utf-8') as f:
        feedback_data = yaml.safe_load(f)
    
    if 'flows' in feedback_data and 'give_feedback' in feedback_data['flows']:
        if 'nlu_trigger' not in feedback_data['flows']['give_feedback']:
            # Insert nlu_trigger before steps (by just adding it to dict)
            feedback_data['flows']['give_feedback']['nlu_trigger'] = [{'intent': 'give_feedback'}]
            with open(feedback_file, 'w', encoding='utf-8') as f:
                yaml.safe_dump(feedback_data, f, allow_unicode=True, sort_keys=False, width=1000)
            print("Added nlu_trigger to give_feedback flow")

# 3. Add nlu_trigger to show_faqs.yml if missing
faqs_file = general_dir / 'show_faqs.yml'
if faqs_file.exists():
    with open(faqs_file, 'r', encoding='utf-8') as f:
        faqs_data = yaml.safe_load(f)
    
    if 'flows' in faqs_data and 'search_faq_by_keyword' in faqs_data['flows']:
        if 'nlu_trigger' not in faqs_data['flows']['search_faq_by_keyword']:
            faqs_data['flows']['search_faq_by_keyword']['nlu_trigger'] = [{'intent': 'faq_search'}]
            with open(faqs_file, 'w', encoding='utf-8') as f:
                yaml.safe_dump(faqs_data, f, allow_unicode=True, sort_keys=False, width=1000)
            print("Added nlu_trigger to search_faq_by_keyword flow")

# 4. Move all files in general to flows
for f in general_dir.glob('*.yml'):
    if f.is_file():
        dest = flows_dir / f.name
        shutil.move(str(f), str(dest))
        print(f"Moved {f.name} to {flows_dir}")

# Remove empty general directory
if general_dir.exists() and not any(general_dir.iterdir()):
    general_dir.rmdir()

# 5. Clean conflicting rules
if rules_file.exists():
    with open(rules_file, 'r', encoding='utf-8') as f:
        rules_data = yaml.safe_load(f)
    
    intents_to_remove = ['greet', 'goodbye', 'ask_help', 'give_feedback', 'faq_search']
    
    if 'rules' in rules_data:
        original_count = len(rules_data['rules'])
        rules_data['rules'] = [
            rule for rule in rules_data['rules'] 
            if not any(step.get('intent') in intents_to_remove for step in rule.get('steps', []))
        ]
        removed_count = original_count - len(rules_data['rules'])
        
        with open(rules_file, 'w', encoding='utf-8') as f:
            yaml.safe_dump(rules_data, f, allow_unicode=True, sort_keys=False, width=1000)
        
        print(f"Removed {removed_count} conflicting rules from rules.yml")

print("Data directory cleanup complete!")
