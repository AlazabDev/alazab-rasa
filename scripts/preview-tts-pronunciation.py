from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
LEXICON_FILE = ROOT_DIR / "piper" / "pronunciation_lexicon.yml"

DEFAULT_TEXTS = [
    "مرحباً بعميلنا العزيز، شكراً لاتصالكم بمؤسسة العزب للهندسة المعمارية. أنا بوت العزب.",
    "Alazab Group تجمع التنفيذ المعماري والتشطيبات الراقية وإدارة الصيانة والتشغيل.",
    "Luxury Finishing تقدم التشطيبات الداخلية الراقية والتنفيذ الفاخر.",
    "Brand Identity تساعدك في تصميم الهوية التجارية وإدارة سلاسل الإمداد.",
    "يمكنك تقديم طلب صيانة مباشر من خلال UberFix.",
    "Laban Alasfour متخصصة في توريد الخامات للمشروعات المعمارية.",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview Alazab TTS pronunciation normalization.")
    parser.add_argument("text", nargs="*", help="Optional text to normalize. If omitted, built-in samples are used.")
    parser.add_argument("--tts-url", help="Optional TTS endpoint, for example http://127.0.0.1:8000/chat/tts")
    parser.add_argument("--out-dir", default=str(ROOT_DIR / "piper" / "generated-samples"), help="Output directory for generated mp3 samples.")
    parser.add_argument("--voice", default="nova", help="Server TTS voice when --tts-url is used.")
    args = parser.parse_args()

    rules = load_rules(LEXICON_FILE)
    samples = [" ".join(args.text)] if args.text else DEFAULT_TEXTS

    for index, sample in enumerate(samples, start=1):
        normalized = apply_rules(sample, rules)
        print(f"--- Sample {index}")
        print(f"IN : {sample}")
        print(f"OUT: {normalized}")
        if args.tts_url:
            output_path = Path(args.out_dir) / f"sample-{index:02d}.mp3"
            generate_tts_sample(args.tts_url, normalized, output_path, args.voice)
            print(f"MP3: {output_path}")


def load_rules(path: Path) -> list[tuple[str, str]]:
    if not path.exists():
        raise SystemExit(f"Lexicon file not found: {path}")

    matches: list[str] = []
    current_written: str | None = None
    rules: list[tuple[str, str]] = []
    in_match_block = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("- id:"):
            matches = []
            current_written = None
            in_match_block = False
            continue

        if line.startswith("- written:"):
            current_written = yaml_scalar(line.split(":", 1)[1].strip())
            in_match_block = False
            continue

        if line.startswith("preferred_spoken:") and current_written:
            rules.append((current_written, yaml_scalar(line.split(":", 1)[1].strip())))
            current_written = None
            continue

        if line == "match:":
            in_match_block = True
            continue

        if line.startswith("say_as:"):
            target = yaml_scalar(line.split(":", 1)[1].strip())
            rules.extend((match, target) for match in matches)
            matches = []
            in_match_block = False
            continue

        if in_match_block and line.startswith("- "):
            matches.append(yaml_scalar(line[2:].strip()))

    return sorted(rules, key=lambda item: len(item[0]), reverse=True)


def apply_rules(text: str, rules: list[tuple[str, str]]) -> str:
    output = text
    for source, target in rules:
        output = re.sub(re.escape(source), target, output)
    return output


def yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def generate_tts_sample(tts_url: str, text: str, output_path: Path, voice: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({"text": text, "voice": voice}, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        tts_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            if response.status != 200:
                raise SystemExit(f"TTS failed with status {response.status}")
            output_path.write_bytes(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"TTS HTTP error {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"TTS connection failed: {exc.reason}") from exc


if __name__ == "__main__":
    main()
