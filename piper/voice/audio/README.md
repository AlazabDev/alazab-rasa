# Audio Files — مجموعة العزب

هذا المجلد يحتوي على الملفات الصوتية للبراندات.

## الملفات المطلوبة (من audio_assets_manifest.json)

### samples/
- sample-azabot-v01.mp3 / .wav / .flac
- sample-azabot-v02.mp3 / .wav / .flac
- sample-hazem-polished-arabic-care-v02.mp3
- sample-polished-arabic-customer-care-v01.mp3 / .wav

### voice-brands/
- alazab_construction/ar-voice-alazab-core.mp3
- brand_identity/brand-identity.mp3
- laban_alasfour/ar-voice-laban-alasfour.mp3
- luxury_finishing/luxury-finishing.mp3
- uberfix/brand-05-uberfix-master-v01.wav

## إعادة التوليد

```bash
# باستخدام OpenAI TTS
cd ~/azabot/alazab-rasa
source .venv/bin/activate
python3 piper/generate_brand_samples.py --engine openai

# أو باستخدام Piper (يحتاج تحميل النماذج أولاً)
python3 piper/generate_brand_samples.py --engine piper
```

## تحميل نماذج Piper

```bash
# ar_JO-kareem-medium (الصوت الرئيسي)
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx \
     -O piper/ar_JO-kareem-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/ar/ar_JO/kareem/medium/ar_JO-kareem-medium.onnx.json \
     -O piper/ar_JO-kareem-medium.onnx.json
```
