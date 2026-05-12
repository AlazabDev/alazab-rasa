import os
import json
import re
import argparse
from pathlib import Path
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PIPER_DIR = Path(__file__).parent
ROOT_DIR = PIPER_DIR.parent
LEXICON_FILE = PIPER_DIR / "pronunciation_lexicon.yml"
BRANDS_JSON = PIPER_DIR / "voice" / "code" / "voice_scripts_by_brand.json"
OUTPUT_DIR = PIPER_DIR / "voice" / "audio"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value

def load_rules(path: Path) -> list[tuple[str, str]]:
    if not path.exists():
        return []
    
    rules = []
    current_written = None
    lines = path.read_text(encoding="utf-8").splitlines()
    
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        
        # Simple format support
        if stripped.startswith("- source:"):
            current_written = yaml_scalar(stripped.split(":", 1)[1])
            continue
        if stripped.startswith("target:") and current_written:
            rules.append((current_written, yaml_scalar(stripped.split(":", 1)[1])))
            current_written = None
            continue
            
    # Sort by length descending to match longest phrases first
    return sorted(rules, key=lambda x: len(x[0]), reverse=True)

def apply_rules(text: str, rules: list[tuple[str, str]]) -> str:
    output = text
    for source, target in rules:
        output = re.sub(re.escape(source), target, output)
    return output

async def generate_audio(text: str, filename: str, voice: str = "nova"):
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY not found in .env")
        return
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / filename
    
    print(f"Generating audio for: {filename}...")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/audio/speech",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "tts-1",
                "voice": voice,
                "input": text
            },
            timeout=60.0
        )
        
        if response.status_code == 200:
            output_path.write_bytes(response.content)
            print(f"Success! Saved to {output_path}")
        else:
            print(f"Error {response.status_code}: {response.text}")

async def main():
    parser = argparse.ArgumentParser(description="Generate brand audio samples using normalized text.")
    parser.add_argument("--voice", default="nova", help="OpenAI TTS voice (nova, shimer, alloy, etc.)")
    args = parser.parse_args()

    rules = load_rules(LEXICON_FILE)
    print(f"Loaded {len(rules)} pronunciation rules.")

    if not BRANDS_JSON.exists():
        print(f"Error: {BRANDS_JSON} not found.")
        return

    brands = json.loads(BRANDS_JSON.read_text(encoding="utf-8"))
    
    for brand in brands:
        brand_id = brand["brand_id"]
        script = brand["script_ar"]
        
        normalized = apply_rules(script, rules)
        
        print(f"\n--- Brand: {brand['brand_ar']} ({brand_id})")
        print(f"Original: {script[:50]}...")
        print(f"Normalized: {normalized[:50]}...")
        
        filename = f"{brand_id.replace('_', '-')}.mp3"
        await generate_audio(normalized, filename, voice=args.voice)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
