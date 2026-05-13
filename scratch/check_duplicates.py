import yaml
import os
from collections import defaultdict

def check_duplicates(root_dir):
    all_responses = defaultdict(list)
    all_intents = defaultdict(list)
    all_actions = defaultdict(list)
    all_slots = defaultdict(list)
    all_forms = defaultdict(list)

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.yml'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        if not data: continue
                        
                        if 'responses' in data:
                            for k in data['responses']:
                                all_responses[k].append(file)
                        if 'intents' in data:
                            for k in data['intents']:
                                # intents can be a list or a dict
                                if isinstance(k, str):
                                    all_intents[k].append(file)
                                elif isinstance(k, dict):
                                    for ik in k:
                                        all_intents[ik].append(file)
                        if 'actions' in data:
                            for k in data['actions']:
                                all_actions[k].append(file)
                        if 'slots' in data:
                            for k in data['slots']:
                                all_slots[k].append(file)
                        if 'forms' in data:
                            for k in data['forms']:
                                all_forms[k].append(file)
                except Exception as e:
                    print(f"Error reading {file}: {e}")

    def report(name, d):
        dupes = {k: v for k, v in d.items() if len(v) > 1}
        if dupes:
            print(f"\nDuplicate {name}:")
            for k, v in dupes.items():
                print(f"  {k}: found in {', '.join(v)}")
        else:
            print(f"\nNo duplicate {name} found.")

    report("Responses", all_responses)
    report("Intents", all_intents)
    report("Actions", all_actions)
    report("Slots", all_slots)
    report("Forms", all_forms)

if __name__ == "__main__":
    domain_root = '/home/azab/azabot/alazab-rasa/domain'
    check_duplicates(domain_root)
