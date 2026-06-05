import os
import yaml
from pathlib import Path
from collections import defaultdict

ROOT = Path("data")

BRANDS_NLU_FILES = [
    "brands/alazab_construction_nlu.yml",
    "brands/brand_identity_nlu.yml",
    "brands/laban_alasfour_nlu.yml",
    "brands/luxury_nlu.yml",
    "brands/uberfix_nlu.yml",
    "brands/nlu.yml",
    "nlu/brands_nlu.yml"
]

GENERAL_NLU_FILES = [
    "general/nlu.yml",
    "nlu/general_nlu.yml",
    "nlu/generated_refined.yml",
    "nlu/uberfix_missing.yml"
]

def load_yaml(file_path):
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def merge_nlu(files):
    intents = defaultdict(set)
    lookups = defaultdict(set)
    
    for f_path in files:
        full_path = ROOT / f_path
        data = load_yaml(full_path)
        if "nlu" in data:
            for item in data["nlu"]:
                if "intent" in item:
                    intent = item["intent"]
                    # examples is a multiline string usually
                    examples = item.get("examples", "")
                    for line in examples.splitlines():
                        line = line.strip()
                        if line.startswith("- "):
                            intents[intent].add(line)
                elif "lookup" in item:
                    lookup_name = item["lookup"]
                    examples = item.get("examples", "")
                    for line in examples.splitlines():
                        line = line.strip()
                        if line.startswith("- "):
                            lookups[lookup_name].add(line)
    return intents, lookups

def save_nlu(filepath, intents, append_version=True):
    os.makedirs(filepath.parent, exist_ok=True)
    nlu_list = []
    for intent, examples in sorted(intents.items()):
        ex_str = "\n".join(sorted(list(examples))) + "\n"
        nlu_list.append({"intent": intent, "examples": ex_str})
    
    out = {}
    if append_version:
        out["version"] = "3.1"
    out["nlu"] = nlu_list
    
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.safe_dump(out, f, allow_unicode=True, sort_keys=False)

def save_lookups(filepath, lookups):
    os.makedirs(filepath.parent, exist_ok=True)
    nlu_list = []
    for lookup, examples in sorted(lookups.items()):
        ex_str = "\n".join(sorted(list(examples))) + "\n"
        nlu_list.append({"lookup": lookup, "examples": ex_str})
        
    out = {"version": "3.1", "nlu": nlu_list}
    
    # Read existing lookups if any
    if filepath.exists():
        existing = load_yaml(filepath)
        if "nlu" in existing:
            for item in existing["nlu"]:
                if "lookup" in item:
                    lookup_name = item["lookup"]
                    for line in item.get("examples", "").splitlines():
                        line = line.strip()
                        if line.startswith("- "):
                            lookups[lookup_name].add(line)
                            
    # Regenerate list
    nlu_list = []
    for lookup, examples in sorted(lookups.items()):
        ex_str = "\n".join(sorted(list(examples))) + "\n"
        nlu_list.append({"lookup": lookup, "examples": ex_str})
    out["nlu"] = nlu_list
    
    with open(filepath, "w", encoding="utf-8") as f:
        yaml.safe_dump(out, f, allow_unicode=True, sort_keys=False)


if __name__ == "__main__":
    print("Merging Brands NLU...")
    brands_intents, brands_lookups = merge_nlu(BRANDS_NLU_FILES)
    save_nlu(ROOT / "nlu/brands_nlu.yml", brands_intents)
    
    print("Merging General NLU...")
    general_intents, general_lookups = merge_nlu(GENERAL_NLU_FILES)
    save_nlu(ROOT / "nlu/general_nlu.yml", general_intents)
    
    print("Merging Lookups...")
    all_lookups = defaultdict(set)
    for k, v in brands_lookups.items(): all_lookups[k].update(v)
    for k, v in general_lookups.items(): all_lookups[k].update(v)
    save_lookups(ROOT / "nlu/lookups.yml", all_lookups)
    
    # Delete old files
    print("Deleting old files...")
    all_files = set(BRANDS_NLU_FILES + GENERAL_NLU_FILES)
    for f in all_files:
        full_path = ROOT / f
        # Don't delete the targets!
        if f not in ["nlu/brands_nlu.yml", "nlu/general_nlu.yml", "nlu/lookups.yml"]:
            if full_path.exists():
                os.remove(full_path)
                print(f"Deleted {f}")

    print("Done!")
