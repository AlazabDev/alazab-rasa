import os
import yaml
from pathlib import Path
from collections import defaultdict

ROOT = Path("domain")

FILES_TO_MERGE = [
    "general/feedback.yml",
    "general/goodbye.yml",
    "general/hello.yml",
    "general/help.yml",
    "general/human_handoff.yml",
    "general/maintenance.yml",
    "general/placeholder_domain.yml",
    "general/privacy.yml",
    "general/show_faqs.yml",
    "maintenance_request.yml"
]

def load_yaml(file_path):
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def main():
    target_file = ROOT / "general.yml"
    merged = load_yaml(target_file)
    
    # Initialize keys if missing
    if "responses" not in merged:
        merged["responses"] = {}
    if "slots" not in merged:
        merged["slots"] = {}
    if "actions" not in merged:
        merged["actions"] = []

    for rel in FILES_TO_MERGE:
        path = ROOT / rel
        if path.exists():
            data = load_yaml(path)
            if "responses" in data:
                for r_key, r_val in data["responses"].items():
                    merged["responses"][r_key] = r_val
            if "slots" in data:
                for s_key, s_val in data["slots"].items():
                    merged["slots"][s_key] = s_val
            if "actions" in data:
                for a in data["actions"]:
                    if a not in merged["actions"]:
                        merged["actions"].append(a)

    with open(target_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(merged, f, allow_unicode=True, sort_keys=False, width=1000)

    # Now delete the merged files
    for rel in FILES_TO_MERGE:
        path = ROOT / rel
        if path.exists():
            os.remove(path)
            print(f"Deleted {path}")

    print("Domain merging completed!")

if __name__ == "__main__":
    main()
