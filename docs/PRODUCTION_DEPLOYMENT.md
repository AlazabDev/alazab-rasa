# Production Deployment

## Project Structure

- Rasa backend: `config.yml`, `domain.yml`, `credentials.yml`, `endpoints.yml`, `data/`, `actions/`, `tests/`.
- Production scripts: `scripts/prod-check.sh`, `scripts/train-prod.sh`, `scripts/run-rasa-prod.sh`, `scripts/run-actions-prod.sh`.
- Supabase project: `azabot/supabase/` with migrations in `azabot/supabase/migrations/` and edge functions in `azabot/supabase/functions/`.
- Frontend/admin app: `azabot/`.

## Validation

Run from the repository root:

```bash
chmod +x scripts/*.sh
bash scripts/prod-check.sh
rasa data validate
```

`prod-check.sh` verifies Python, Rasa, required project files, Rasa domain/data validity, action imports, the linked Supabase project ref, functions, and migrations.

## Training

```bash
bash scripts/train-prod.sh
```

The script activates `.venv` when available, validates data, runs `rasa train --force`, and writes the model artifact to `models/`.

## Running Rasa

```bash
RASA_PORT=5005 bash scripts/run-rasa-prod.sh
```

The server binds to `127.0.0.1` by default, uses `endpoints.yml` and `credentials.yml`, and enables the HTTP API. Set `RASA_CORS` only to the origins needed by the reverse proxy or frontend.

## Running Actions

```bash
ACTION_PORT=5055 bash scripts/run-actions-prod.sh
```

The action server binds to `127.0.0.1` by default and loads the `actions` package.

## Supabase Cloud

The linked project ref is read from `azabot/supabase/.temp/project-ref`. Do not use `supabase status` for cloud validation.

```bash
bash scripts/supabase-cloud-sync.sh
```

The script runs `supabase migration list`, `supabase db push`, and deploys each deployable folder in `azabot/supabase/functions/`. `_shared` is skipped because it is support code, not an edge function.

## systemd Notes

Use a restricted service user and an environment file outside source control. Example commands:

```bash
sudo systemctl daemon-reload
sudo systemctl enable alazab-rasa-actions alazab-rasa-server
sudo systemctl restart alazab-rasa-actions alazab-rasa-server
sudo journalctl -u alazab-rasa-server -f
```

The existing service templates live in `deploy/systemd/`. Point `ExecStart` to the production runner scripts or equivalent `.venv/bin/rasa` commands, and keep services bound to `127.0.0.1`.

## Nginx Notes

Terminate TLS at Nginx and proxy only the needed paths to local services:

- Rasa REST/API: `http://127.0.0.1:5005`
- Webhook/FastAPI service, if used: `http://127.0.0.1:8000`
- Frontend static app or Vite build output from `azabot/dist`

Set request size limits for uploads and forward `X-Forwarded-Proto`, `X-Forwarded-For`, and `Host`.

## Rollback

- Rasa: keep the previous model artifact in `models/`; restart Rasa with the previous model if a new model regresses.
- Supabase migrations: prefer forward-fix migrations. If rollback is required, prepare a reviewed SQL rollback and apply it manually through the Supabase SQL editor or CLI.
- Functions: redeploy the previous known-good commit with `supabase functions deploy <name>`.
- Services: use `systemctl restart` after reverting code or environment changes.

## Troubleshooting

- `rasa` not found: activate `.venv` or install dependencies from `requirements.txt`.
- Action import failure: run `PYTHONDONTWRITEBYTECODE=1 python -c "import actions"` and inspect the missing import.
- Rasa validation failure: fix missing intents, actions, responses, slots, or invalid stories/rules before training.
- Supabase command hangs or fails: verify CLI login, network access, and `azabot/supabase/.temp/project-ref`.
- Redis tracker issues: check `endpoints.yml` and production Redis credentials.
- External API failures: verify `.env` values for OpenAI, Meta/WhatsApp, Telegram, UberFix, Daftra, and Supabase.
