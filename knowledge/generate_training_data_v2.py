import json
import os
import yaml

def generate_nlu_data():
    base_dir = "/home/azab/azabot/alazab-rasa/"
    input_json = os.path.join(base_dir, "knowledge/production/alazab_kb.json")
    output_dir = os.path.join(base_dir, "data/nlu/")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Create Lookup Tables
    items_lookup = set()
    actions_lookup = set()
    categories_lookup = set()

    for entry in data:
        item = entry.get('item', '').strip()
        action = entry.get('action', '').strip()
        category = entry.get('category', '').strip()

        if item and len(item) < 100: # Filter out very long descriptions for lookup
            items_lookup.add(item)
        if action and action != "other":
            actions_lookup.add(action)
        if category:
            categories_lookup.add(category)

    # 2. Generate NLU Structure
    nlu_content = {
        "version": "3.1",
        "nlu": []
    }

    # Add Lookups
    nlu_content["nlu"].append({
        "lookup": "service_item",
        "examples": "\n".join([f"- {i}" for i in sorted(list(items_lookup))])
    })
    
    nlu_content["nlu"].append({
        "lookup": "action_type",
        "examples": "\n".join([f"- {a}" for a in sorted(list(actions_lookup))])
    })

    # 3. Add Intent Examples (Templated from real items)
    intent_examples = {
        "ask_alazab_technical_specs": [],
        "ask_uberfix_request": [],
        "ask_alazab_quote": []
    }

    # Samples for training
    sample_items = list(items_lookup)[:50] # Take first 50 diverse items
    
    for item in sample_items:
        intent_examples["ask_alazab_technical_specs"].append(f"- ماهي مواصفات [ {item} ](service_item)؟")
        intent_examples["ask_alazab_technical_specs"].append(f"- محتاج اعرف تفاصيل عن [ {item} ](service_item)")
        
        intent_examples["ask_uberfix_request"].append(f"- محتاج [ صيانة ](action_type) لـ [ {item} ](service_item)")
        intent_examples["ask_uberfix_request"].append(f"- عندي مشكلة في [ {item} ](service_item)")
        
        intent_examples["ask_alazab_quote"].append(f"- سعر [ توريد وتركيب ](action_type) [ {item} ](service_item) كام؟")
        intent_examples["ask_alazab_quote"].append(f"- محتاج عرض سعر لـ [ {item} ](service_item)")

    for intent, examples in intent_examples.items():
        nlu_content["nlu"].append({
            "intent": intent,
            "examples": "\n".join(examples)
        })

    # Save to file
    output_path = os.path.join(output_dir, "generated_refined_data.yml")
    
    # Custom representer to handle Arabic and long strings nicely
    class QuotedString(str): pass
    def quoted_presenter(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    yaml.add_representer(QuotedString, quoted_presenter)

    with open(output_path, 'w', encoding='utf-8') as f:
        # We manually format to ensure the "-" list style Rasa likes
        f.write("version: \"3.1\"\n\nnlu:\n")
        
        # Write Lookups
        for item in nlu_content["nlu"]:
            if "lookup" in item:
                f.write(f"- lookup: {item['lookup']}\n  examples: |\n")
                for ex in item['examples'].split("\n"):
                    f.write(f"    {ex}\n")
            elif "intent" in item:
                f.write(f"- intent: {item['intent']}\n  examples: |\n")
                for ex in item['examples'].split("\n"):
                    f.write(f"    {ex}\n")

    print(f"NLU Generation Complete: {output_path}")

if __name__ == "__main__":
    generate_nlu_data()
