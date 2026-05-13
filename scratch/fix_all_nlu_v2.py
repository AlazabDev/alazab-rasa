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
        # Handle top-level list items (intent, lookup, etc.)
        if stripped.startswith('- intent:') or stripped.startswith('- lookup:'):
            new_lines.append('  ' + stripped + '\n')
            in_examples = False
        # Handle examples: block
        elif stripped.startswith('examples:'):
            # Find current indentation of the previous line if possible, or assume 2
            new_lines.append('    examples: |\n')
            in_examples = True
            # Extract inline example if present
            if "'- " in line:
                text = line.split("'- ", 1)[1].strip().rstrip("'")
                if text:
                    new_lines.append('      - ' + text + '\n')
            elif ": -" in line:
                text = line.split(": -", 1)[1].strip().rstrip("'")
                if text:
                    new_lines.append('      - ' + text + '\n')
        # Handle list items within examples
        elif stripped.startswith('- ') and in_examples:
            content = stripped[2:].strip().strip("'").strip('"')
            new_lines.append('      - ' + content + '\n')
        # Handle plain text within examples (if they weren't starting with -)
        elif in_examples and stripped and not stripped.startswith('version:') and not stripped.startswith('nlu:'):
            content = stripped.strip("'").strip('"')
            new_lines.append('      - ' + content + '\n')
        # Handle root keys
        elif stripped == 'nlu:':
            new_lines.append('nlu:\n')
        elif stripped.startswith('version:'):
            new_lines.append(line)
        # Preserve empty lines or other stuff
        else:
            if not stripped:
                new_lines.append('\n')
            else:
                new_lines.append(line)

    with open(abs_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

for f in files:
    fix_file(f)
