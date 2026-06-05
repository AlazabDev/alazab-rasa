import yaml
import os

brands_to_merge = ["uberfix", "laban_alasfour", "luxury_finishing", "brand_identity"]

for brand in brands_to_merge:
    brand_file = f"data/brands/{brand}.yml"
    flow_file = f"data/flows/{brand}.yml"
    
    if not os.path.exists(brand_file) or not os.path.exists(flow_file):
        continue
        
    with open(brand_file, "r", encoding="utf-8") as f:
        brand_data = yaml.safe_load(f) or {}
        
    with open(flow_file, "r", encoding="utf-8") as f:
        flow_data = yaml.safe_load(f) or {}
        
    # Merge flows
    if "flows" in flow_data:
        if "flows" not in brand_data:
            brand_data["flows"] = {}
        for flow_name, flow_content in flow_data["flows"].items():
            brand_data["flows"][flow_name] = flow_content
            
    with open(brand_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(brand_data, f, allow_unicode=True, sort_keys=False)
        
    print(f"Merged {brand}.yml successfully.")
