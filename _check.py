"""فحص شامل لجاهزية المشروع"""
import sys, os, yaml, glob

sys.path.insert(0, ".")
ROOT = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print("1. ACTIONS IMPORT")
print("=" * 60)
try:
    from actions import action_general, action_human_handoff, action_submit_lead
    from actions import action_daftra_ops, action_uberfix_ops, action_brand_navigator
    from actions import action_context_accumulator, action_send_sweets_info
    from actions.brand_actions import alazab_construction, brand_identity
    from actions.brand_actions import laban_alasfour, luxury_finishing, uberfix
    from actions.maintenance import MaintenanceService
    print("ALL ACTIONS: OK")
except Exception as e:
    print(f"ACTION ERROR: {e}")

print()
print("=" * 60)
print("2. KNOWLEDGE PATHS")
print("=" * 60)
from actions.config import PROD_DATA_PATH, CATEGORIES_PATH
kb_path = os.path.join(PROD_DATA_PATH, "alazab_kb.json")
print(f"PROD_DATA_PATH exists: {os.path.exists(PROD_DATA_PATH)}")
print(f"CATEGORIES_PATH exists: {os.path.exists(CATEGORIES_PATH)}")
print(f"alazab_kb.json exists: {os.path.exists(kb_path)}")

print()
print("=" * 60)
print("3. YAML SYNTAX")
print("=" * 60)
yaml_errors = []
for f in glob.glob("domain/**/*.yml", recursive=True) + glob.glob("data/**/*.yml", recursive=True):
    try:
        with open(f, encoding="utf-8") as fh:
            yaml.safe_load(fh)
    except Exception as e:
        yaml_errors.append(f"  ERR: {f.replace(ROOT, '')} -> {e}")
if yaml_errors:
    for e in yaml_errors:
        print(e)
else:
    print("ALL YAML FILES: OK")

print()
print("=" * 60)
print("4. INTENTS COVERAGE")
print("=" * 60)
# جمع intents من domain
domain_intents = set()
for f in ["domain.yml", "domain/general.yml"]:
    try:
        with open(f, encoding="utf-8") as fh:
            d = yaml.safe_load(fh)
        if d and "intents" in d:
            domain_intents.update(d["intents"])
    except:
        pass

# جمع intents من NLU
nlu_intents = set()
for f in glob.glob("data/**/*.yml", recursive=True):
    try:
        with open(f, encoding="utf-8") as fh:
            d = yaml.safe_load(fh)
        if d and "nlu" in d and d["nlu"]:
            for item in d["nlu"]:
                if isinstance(item, dict) and "intent" in item:
                    nlu_intents.add(item["intent"])
    except:
        pass

skip = {"session_start", "nlu_fallback"}
missing_nlu = domain_intents - nlu_intents - skip
missing_domain = nlu_intents - domain_intents

print(f"Domain intents total: {len(domain_intents)}")
print(f"NLU intents total:    {len(nlu_intents)}")
if missing_nlu:
    print(f"\nIN DOMAIN BUT NO NLU ({len(missing_nlu)}):")
    for i in sorted(missing_nlu):
        print(f"  - {i}")
else:
    print("ALL DOMAIN INTENTS HAVE NLU: OK")

if missing_domain:
    print(f"\nIN NLU BUT NOT IN DOMAIN ({len(missing_domain)}):")
    for i in sorted(missing_domain):
        print(f"  - {i}")
else:
    print("ALL NLU INTENTS IN DOMAIN: OK")

print()
print("=" * 60)
print("5. ACTIONS IN DOMAIN vs CODE")
print("=" * 60)
# جمع actions من domain.yml
dom_actions = set()
try:
    with open("domain.yml", encoding="utf-8") as fh:
        d = yaml.safe_load(fh)
    if d and "actions" in d:
        dom_actions.update(d["actions"])
except:
    pass

# جمع action names من الكود
code_actions = set()
for f in glob.glob("actions/**/*.py", recursive=True):
    try:
        with open(f, encoding="utf-8") as fh:
            content = fh.read()
        import re
        names = re.findall(r'return\s+"(action_[^"]+|validate_[^"]+)"', content)
        code_actions.update(names)
    except:
        pass

ghost_actions = dom_actions - code_actions
print(f"Domain actions: {len(dom_actions)}")
print(f"Code actions:   {len(code_actions)}")
if ghost_actions:
    print(f"\nIN DOMAIN BUT NOT IN CODE ({len(ghost_actions)}):")
    for a in sorted(ghost_actions):
        print(f"  - {a}")
else:
    print("ALL DOMAIN ACTIONS EXIST IN CODE: OK")

print()
print("=" * 60)
print("DONE")
print("=" * 60)
