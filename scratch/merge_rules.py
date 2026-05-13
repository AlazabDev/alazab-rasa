import yaml
import os

def merge_yaml_files(file1, file2, output_file, key):
    with open(file1, 'r', encoding='utf-8') as f1:
        data1 = yaml.safe_load(f1)
    with open(file2, 'r', encoding='utf-8') as f2:
        data2 = yaml.safe_load(f2)
    
    merged_data = data1.copy()
    if key in data2:
        if key not in merged_data:
            merged_data[key] = []
        # Rules are lists
        merged_data[key].extend(data2[key])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(merged_data, f, allow_unicode=True, sort_keys=False)

rules_path = '/home/azab/azabot/alazab-rasa/data/rules'
# Just rename them for now as they seem to be distinct domains
# But I will move the classic_rules.yml to a common place if needed.
