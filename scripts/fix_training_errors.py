import os
from pathlib import Path

def replace_in_file(filepath, old_str, new_str):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if old_str in content:
        content = content.replace(old_str, new_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

def main():
    root = Path("data")
    
    # Files to process
    target_files = [
        root / "stories" / "classic_stories.yml",
        root / "rules" / "brands_rules.yml",
        root / "rules" / "classic_rules.yml"
    ]
    
    for file in target_files:
        if file.exists():
            replace_in_file(file, "action: utter_thanks\n", "action: utter_closing_words\n")
            replace_in_file(file, "action: utter_default_fallback\n", "action: action_default_fallback\n")

if __name__ == "__main__":
    main()
