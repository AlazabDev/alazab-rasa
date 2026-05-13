import yaml
import sys

file_path = '/home/azab/azabot/alazab-rasa/data/nlu/brands_nlu.yml'

with open(file_path, 'r', encoding='utf-8') as f:
    try:
        data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML: {e}")
        # If it's broken, we might need a more robust way to fix it.
        # Let's try to fix it line by line.
        f.seek(0)
        lines = f.readlines()
        new_lines = []
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith('- intent:'):
                new_lines.append('  ' + stripped)
            elif stripped.startswith('examples:'):
                new_lines.append('    ' + stripped)
            elif stripped.startswith('- ') and not stripped.startswith('- intent:'):
                new_lines.append('      ' + stripped)
            elif stripped.strip() == 'nlu:':
                new_lines.append('nlu:\n')
            elif stripped.startswith('version:'):
                new_lines.append(line)
            else:
                new_lines.append(line)
        
        with open(file_path, 'w', encoding='utf-8') as f2:
            f2.writelines(new_lines)
        sys.exit(0)

# If it loaded successfully, we can just dump it back.
with open(file_path, 'w', encoding='utf-8') as f:
    yaml.dump(data, f, allow_unicode=True, sort_keys=False)
