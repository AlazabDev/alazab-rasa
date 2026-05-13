import yaml
import sys

file_path = '/home/azab/azabot/alazab-rasa/data/nlu/general_nlu.yml'

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
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
            # If it was examples: '- text', extract text
            if "'- " in line:
                text = line.split("'- ", 1)[1].strip().rstrip("'")
                new_lines.append('      - ' + text + '\n')
            in_examples = True
        elif stripped.startswith('- ') and in_examples:
            new_lines.append('      - ' + stripped[2:].strip().rstrip("'") + '\n')
        elif stripped == "'": # Stray quote
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
    
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

fix_file('/home/azab/azabot/alazab-rasa/data/nlu/general_nlu.yml')
fix_file('/home/azab/azabot/alazab-rasa/data/nlu/brands_nlu.yml')
