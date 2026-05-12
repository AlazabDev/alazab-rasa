import os
import re

def fix_yaml_pipes(file_path):
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    changed = False
    for line in lines:
        # Regex to match '  - text: | Some text' or '  text: | Some text'
        # Group 1: Leading whitespace
        # Group 2: Prefix (e.g., "- text: " or "text: ")
        # Group 3: Pipe or Folded symbol (| or >)
        # Group 4: The text after the symbol
        match = re.match(r'^(\s*)(.*text:\s*)(\||>)\s*(.+)$', line)
        if match:
            indent = match.group(1)
            prefix = match.group(2)
            symbol = match.group(3)
            text = match.group(4)
            
            # The new format should have the text on the next line, indented further
            new_lines.append(f"{indent}{prefix}{symbol}\n")
            new_lines.append(f"{indent}    {text}\n")
            changed = True
        else:
            new_lines.append(line)
    
    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Fixed {file_path}")
    else:
        print(f"No changes needed for {file_path}")

def main():
    root_dir = "/home/azab/azabot/alazab-rasa"
    dirs_to_check = ["domain", "data"]
    
    for d in dirs_to_check:
        full_path = os.path.join(root_dir, d)
        if not os.path.exists(full_path):
            continue
            
        for root, _, files in os.walk(full_path):
            for file in files:
                if file.endswith((".yml", ".yaml")):
                    fix_yaml_pipes(os.path.join(root, file))

if __name__ == "__main__":
    main()
