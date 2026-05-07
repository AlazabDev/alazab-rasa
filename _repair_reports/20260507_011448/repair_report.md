# Rasa WSL Repair Report

- Project root: /home/azab/azabot/alazab-rasa
- Backup dir: /home/azab/azabot/alazab-rasa/_repair_backups/20260507_011448
- Report dir: /home/azab/azabot/alazab-rasa/_repair_reports/20260507_011448
- Python: /home/azab/azabot/alazab-rasa/.venv/bin/python

## What was repaired safely

- UTF-8 BOM removed when found.
- CRLF converted to LF.
- YAML leading tabs converted to spaces.
- Missing `version: "3.1"` added to data YAML files.
- Missing domain keys added if absent.
- Missing NLU intents added to domain.
- Missing custom actions referenced in stories/rules added to domain actions.
- Missing utter responses referenced in stories/rules added with safe placeholder text.
- JSON and JSONL syntax checked.
- Python action files compiled.

## Validation logs

- `/home/azab/azabot/alazab-rasa/_repair_reports/20260507_011448/structure_repair.json`
- `/home/azab/azabot/alazab-rasa/_repair_reports/20260507_011448/rasa_data_validate.log`
- `/home/azab/azabot/alazab-rasa/_repair_reports/20260507_011448/rasa_validate_status.txt`

