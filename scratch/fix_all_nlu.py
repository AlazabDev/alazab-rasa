import yaml
import sys
import os

files = [
    'data/brands/nlu.yml',
    'data/nlu/general_nlu.yml',
    'data/nlu/generated_refined_data.yml',
    'data/nlu/brands_nlu.yml',
    'data/general/nlu.yml'
]

def fix_file(path):
    abs_path = os.path.join('/home/azab/azabot/alazab-rasa', path)
    if not os.path.exists(abs_path):
        print(f"Skipping {abs_path}")
        return
    with open(abs_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    in_examples = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- intent:'):
            new_lines.append('  ' + stripped + '\n')
            in_examples = False
        elif stripped.startswith('examples:'):
            new_lines.append('    examples: |\n')
            if "'- " in line:
                text = line.split("'- ", 1)[1].strip().rstrip("'")
                new_lines.append('      - ' + text + '\n')
            in_examples = True
        elif stripped.startswith('- ') and in_examples:
            new_lines.append('      - ' + stripped[2:].strip().rstrip("'") + '\n')
        elif stripped == "'":
            continue
        elif stripped == 'nlu:':
            new_lines.append('nlu:\n')
        elif stripped.startswith('version:'):
            new_lines.append(line)
        else:
            if in_examples and stripped:
                new_lines.append('      - ' + stripped.rstrip("'") + '\n')
            else:
                new_lines.append(line)
    
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

for f in files:
    fix_file(f)
