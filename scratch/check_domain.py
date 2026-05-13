import yaml
import os

def check_domain_files(root_dir):
    results = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.yml'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        yaml.safe_load(f)
                    results.append((file, "OK", None))
                except Exception as e:
                    results.append((file, "ERROR", str(e)))
    return results

if __name__ == "__main__":
    domain_root = '/home/azab/azabot/alazab-rasa/domain'
    results = check_domain_files(domain_root)
    for file, status, error in results:
        print(f"{file}: {status}")
        if error:
            print(f"  {error}")
