import json
import re
import os

def normalize_arabic(text):
    if not text: return ""
    text = text.strip()
    # Remove "تم عمل", "تم", "اعمال" to get core task
    text = re.sub(r'^(تم عمل|تم|بالمقطوعية|بالعدد|بالمقطوعيه|بالمتر الطوالي|اعمال|بند)\s+', '', text)
    # Remove diacritics
    text = re.sub(r'[\u064B-\u0652]', '', text)
    # Normalize Alefs
    text = re.sub(r'[أإآا]', 'ا', text)
    # Normalize Taa Marbuta
    text = re.sub(r'ة', 'ه', text)
    # Normalize Yaa
    text = re.sub(r'ى', 'ي', text)
    return text.lower()

def refine_inventory(input_file, output_file):
    if not os.path.exists(input_file):
        print("Input file not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    refined = {}
    
    for entry in data:
        desc = entry['clean_description']
        norm_desc = normalize_arabic(desc)
        
        if norm_desc not in refined:
            refined[norm_desc] = {
                "master_description": desc,
                "action": entry['action'],
                "price_models": set(),
                "variations": set(),
                "frequency": 0
            }
        
        group = refined[norm_desc]
        group["frequency"] += 1
        group["variations"].add(entry['raw_text'])
        if entry['price_model'] != 'unknown':
            group["price_models"].add(entry['price_model'])

    # Convert sets to lists for JSON serialization
    final_output = []
    for norm_desc, info in refined.items():
        # Heuristic: the most common description might be the master, 
        # but for now we take the first one encountered.
        final_output.append({
            "task_id": norm_desc.replace(" ", "_"),
            "description": info["master_description"],
            "action": info["action"],
            "pricing_standards": list(info["price_models"]),
            "human_variations": list(info["variations"]),
            "demand_score": info["frequency"]
        })

    # Sort by demand score to show what's most common in the company's history
    final_output.sort(key=lambda x: x['demand_score'], reverse=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2)

    print(f"Refined {len(data)} items into {len(final_output)} unique master tasks.")

if __name__ == "__main__":
    input_path = "/home/azab/azabot/alazab-rasa/production_alazab_kb/inventory_structured.json"
    output_path = "/home/azab/azabot/alazab-rasa/alazab_knowledge_production/master_inventory_refined.json"
    refine_inventory(input_path, output_path)
