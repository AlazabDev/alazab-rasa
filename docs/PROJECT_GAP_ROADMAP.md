# AzaBot / Alazab Rasa — Production Gap & Vulnerability Roadmap

## Purpose

This document is the master plan for closing the remaining security vulnerabilities, operational gaps, and incomplete production paths in `AlazabDev/alazab-rasa`.

The project is structurally strong, but production closure requires a controlled sequence. The rule is simple:

> Do not add new features until all P0 release blockers are closed and verified by automated checks.

---

## Current Baseline

The following hotfixes were already applied before this roadmap was created:

- [x] Added the missing synchronous UberFix proxy handler in `webhook/_uberfix_gateway.py`.
- [x] Converted Daftra invoice actions to async and awaited the Supabase invoice link update in `actions/action_daftra_ops.py`.
- [x] Unified the tracked production endpoint template in `endpoints.yml` around `DATABASE_URL` and Redis locking.
- [x] Aligned `requirements.txt` with Rasa Pro CALM and Rasa SDK dependencies.
- [x] Confirmed that maintenance slots already exist in `domain/general/maintenance.yml` and are included by `domain.yml`.

These fixes improve the baseline but do **not** complete production hardening.

---

## Severity Model

| Level | Meaning | Release Rule |
|---|---|---|
| **P0** | Critical security or boot-path blocker | Must be closed before public deployment |
| **P1** | Functional production gap | Must be closed before declaring the feature complete |
| **P2** | Data governance, scale, and reliability weakness | Close immediately after launch freeze |
| **P3** | Quality automation and long-term maintainability | Add before normal feature development resumes |

---

# Phase 0 — Public Release Blockers

## P0-01 — Protect the UberFix privileged proxy

### Evidence

- Public route: `webhook/server.py` → `POST /uberfix/bot-gateway`.
- The route forwards caller-controlled `action` and `payload` to the unified bot gateway.
- The proxy adds the server-side internal API key before forwarding.
- `webhook/models.py` validates that `action` is not empty, but it does not enforce an action allowlist.

### Risk

An external caller may use the public webhook server as a privileged relay to invoke gateway operations that were intended only for trusted internal callers.

### Required changes

- [ ] Add an explicit allowlist for externally permitted bot actions.
- [ ] Reject unknown actions before forwarding.
- [ ] Require an internal signature or scoped client token for privileged actions.
- [ ] Split public actions from internal workflow actions.
- [ ] Add request-level audit logs with redaction.
- [ ] Add rate limiting for `/uberfix/bot-gateway`.
- [ ] Remove project-specific gateway URL fallbacks in production; production must fail closed when env values are missing.

### Acceptance criteria

- Anonymous caller cannot invoke privileged maintenance transitions or administrative gateway actions.
- Unknown action returns `403` or `422` without reaching the upstream gateway.
- Tests cover public, signed, invalid, and replayed requests.

---

## P0-02 — Fix runtime endpoint generation and enforce one source of truth

### Evidence

- `scripts/render_runtime_domain.py` generates `.runtime/domain.generated.yml`.
- Endpoint copy code appears after `raise SystemExit(main())`, so it is not reached when the script is executed normally.
- The copy source is `endpoints.nodocker.yml`, while the tracked production template was unified in `endpoints.yml`.
- `scripts/botctl.sh` and `deploy/systemd/azabot-rasa.service` expect `.runtime/endpoints.generated.yml`.

### Risk

Production may start with a stale, missing, or unintended endpoint configuration even when `endpoints.yml` looks correct in Git.

### Required changes

- [ ] Move runtime endpoint rendering into `main()` before return.
- [ ] Generate `.runtime/endpoints.generated.yml` from **one** source only: `endpoints.yml`.
- [ ] Render env placeholders explicitly and validate required variables.
- [ ] Validate generated YAML before starting Rasa.
- [ ] Fail startup when `DATABASE_URL`, Redis settings, or required model groups are missing.
- [ ] Remove or archive `endpoints.nodocker.yml` after migration.

### Acceptance criteria

- `python scripts/render_runtime_domain.py` always produces both generated runtime files.
- `rasa data validate --domain .runtime/domain.generated.yml` succeeds.
- Rasa starts only with the expected generated endpoint file.

---

## P0-03 — Normalize systemd deployment paths, users, and service names

### Evidence

- `deploy/systemd/azabot-webhook.service` runs as `azab` from `/opt/azabot`.
- `deploy/systemd/azabot-rasa.service` and `deploy/systemd/azabot-actions.service` run as `azureuser` from `/mnt/apps/alazab-rasa`.
- Operational commands used during deployment may use another repository location.

### Risk

Different services may run different code copies or environments. A successful Git pull in one directory may not update the process actually serving production traffic.

### Required changes

- [ ] Adopt one canonical `APP_ROOT` for all services.
- [ ] Adopt one restricted Linux service user.
- [ ] Use the same `.venv`, `.env`, `logs/`, `.runtime/`, and `models/` locations.
- [ ] Use one service naming convention: `azabot-webhook`, `azabot-rasa`, `azabot-actions`.
- [ ] Add `ReadWritePaths` only for required writable directories.
- [ ] Add a deployment verification command that prints the active Git SHA for each service.

### Acceptance criteria

- All services run from the same commit SHA.
- `systemctl cat` shows one canonical root and one restricted service user.
- Restarting services does not require manual path correction.

---

## P0-04 — Enforce RBAC on admin mutations

### Evidence

- `webhook/routers/admin.py` exposes a generic `/admin/api?action=...` dispatcher.
- The dispatcher requires `_require_admin`, not `_require_super`.
- The same dispatcher can update settings, save/delete integrations, delete conversations, delete orders, create/delete KB collections, and start training.
- `_require_super` is currently used only for selected endpoints such as user and session listing.

### Risk

Any authenticated admin-panel account may perform destructive or infrastructure-level actions beyond its intended role.

### Required changes

- [ ] Define permissions per action.
- [ ] Require `_require_super` for integration mutation, training, deletion, and settings mutation.
- [ ] Restrict read-only roles to reporting endpoints.
- [ ] Add audit entries containing actor, action, target, result, and timestamp.
- [ ] Separate GET reads from POST/DELETE mutations.
- [ ] Add CSRF protection if cookie-based tokens remain supported.

### Acceptance criteria

- Read-only user cannot mutate settings, integrations, KB collections, training, or stored conversations.
- Every destructive action generates an audit log.

---

## P0-05 — Make external webhook verification mandatory in production

### Evidence

- Meta signature verification runs only when `META_SECRET` exists.
- Telegram secret verification runs only when `TG_WEBHOOK_SECRET` exists.
- Missing secrets therefore disable verification instead of blocking startup.

### Risk

A misconfigured production deployment may accept forged incoming webhook messages.

### Required changes

- [ ] Treat Meta and Telegram secrets as mandatory when their channels are enabled.
- [ ] Fail startup in production if a configured channel lacks its verification secret.
- [ ] Add replay/idempotency handling using provider message IDs.
- [ ] Add request body size limits and structured rejection logs.

### Acceptance criteria

- Forged Meta and Telegram requests are rejected.
- Duplicate provider messages are processed once only.

---

## P0-06 — Protect public OpenAI-cost endpoints

### Evidence

- Public routes include `/chat`, `/chat/upload`, `/chat/audio`, `/chat/tts`, and `/chat/tts/stream`.
- Middleware includes basic IP rate limits for several chat prefixes.
- The system still permits public callers to consume transcription and TTS resources.
- Rate limiting fails open when Redis is unavailable.

### Risk

Automated abuse can consume OpenAI budget or overload the service. Redis outage removes protection.

### Required changes

- [ ] Add signed web-client session tokens.
- [ ] Add per-IP and per-session quotas.
- [ ] Add daily cost ceilings per channel.
- [ ] Add stricter limits for audio and TTS endpoints.
- [ ] Decide production behavior when Redis is unavailable: fail closed for expensive routes.
- [ ] Track request cost metrics and rejection counts.

### Acceptance criteria

- Expensive endpoints cannot be called without a valid scoped client session.
- Redis outage does not expose unlimited TTS or transcription requests.

---

## P0-07 — Harden uploads before accepting public files

### Evidence

- `webhook/services/uploads.py` stores uploads locally under `webhook/static/uploads` by default.
- Allowed extensions include `.zip`.
- Allowed MIME types include `application/octet-stream`.
- Files are loaded fully into memory before storage.
- No malware scanning, quarantine, retention, or content-disposition policy is implemented.

### Risk

Uploaded files may create malware, storage exhaustion, decompression-bomb, or data exposure risk.

### Required changes

- [ ] Store uploads outside the served static directory.
- [ ] Disable `.zip` and `application/octet-stream` until a quarantine pipeline exists.
- [ ] Stream uploads with hard size limits instead of loading full content into memory.
- [ ] Add malware scan/quarantine state.
- [ ] Record upload metadata in the database.
- [ ] Add retention and cleanup jobs.
- [ ] Serve downloads only through authenticated or signed URLs.

### Acceptance criteria

- Public uploads cannot be executed or fetched directly from a static path.
- Rejected MIME types, oversized files, and quarantined files are tested.

---

# Phase 1 — Functional Completion

## P1-01 — Complete WhatsApp and Telegram voice ingestion

### Evidence

- Incoming WhatsApp audio handler logs the media ID but contains a TODO instead of downloading and transcribing the file.
- Incoming Telegram voice handler sends a temporary message and logs the file ID but does not complete transcription.

### Required changes

- [ ] Download provider media securely.
- [ ] Enforce audio MIME and size limits.
- [ ] Send audio through the existing transcription pipeline.
- [ ] Forward transcript to Rasa with channel metadata.
- [ ] Store transcript and attachment audit metadata.
- [ ] Return user-facing failure messages.

### Acceptance criteria

- A voice note creates the same maintenance flow as a text message.

---

## P1-02 — Complete KB and upload persistence

### Evidence

- `webhook/services/admin_data.py:list_uploads()` returns an empty list and contains a TODO to move storage to Supabase Storage.
- Admin KB upload handling builds in-memory document metadata but does not persist uploaded files or URL records.

### Required changes

- [ ] Use Supabase Storage or the approved storage backend.
- [ ] Persist upload and KB document metadata.
- [ ] Connect document status to indexing state.
- [ ] Add delete/archive behavior.
- [ ] Add signed download URLs.

### Acceptance criteria

- Uploaded KB documents survive restart and appear in admin listing.
- Document indexing state is visible and testable.

---

## P1-03 — Replace fragile background tasks with a durable queue

### Evidence

- Chat recording, integration dispatch, notifications, audio processing, and admin-triggered training use in-process background execution patterns.

### Risk

Tasks may be lost on restart, worker crash, or deployment.

### Required changes

- [ ] Introduce a durable queue backed by Redis or PostgreSQL/PGMQ.
- [ ] Add retry policy, dead-letter handling, and idempotency keys.
- [ ] Track task status from the admin dashboard.
- [ ] Keep training isolated from request-serving workers.

### Acceptance criteria

- Restart during processing does not lose maintenance, notification, or integration tasks.

---

## P1-04 — Consolidate duplicate UberFix action paths

### Evidence

- The repository contains two overlapping maintenance action families:
  - `actions/brand_actions/maintenance_actions.py`
  - `actions/brand_actions/uberfix.py`

### Required changes

- [ ] Select one canonical create/status flow.
- [ ] Keep only one gateway contract and one slot mapping model.
- [ ] Preserve quote/services/subscription actions only where needed.
- [ ] Add end-to-end tests for create, track, triage, assign, and invoice draft.

### Acceptance criteria

- One documented maintenance request lifecycle is used by website, WhatsApp, Telegram, and voice.

---

# Phase 2 — Data Governance and Reliability

## P2-01 — Audit Supabase migrations and RLS as one governed schema

### Evidence

- The repository contains multiple migrations and both historical and current tables.
- Server-side code uses the service-role client for broad operations.
- Current AzaBot tables enable RLS and add service-role policies, but schema drift must be verified against the cloud project.

### Required changes

- [ ] Produce a schema inventory from the linked Supabase project.
- [ ] Compare cloud schema against tracked migrations.
- [ ] Verify RLS and grants for every table.
- [ ] Keep service-role keys server-side only.
- [ ] Add migration verification to deployment.

### Acceptance criteria

- Cloud schema is reproducible from tracked migrations.
- No public client can access internal tables using anon credentials.

---

## P2-02 — Move integration secrets out of raw integration JSON

### Evidence

- Integration configs can include Telegram bot tokens, WhatsApp access tokens, Twilio tokens, Daftra API keys, and OpenAI API keys.
- Integration records are stored and returned by admin data functions as regular records.

### Required changes

- [ ] Store secret values in an approved secret store or encrypted vault layer.
- [ ] Return masked values to the frontend.
- [ ] Separate editable metadata from secrets.
- [ ] Add secret rotation workflow.
- [ ] Redact secrets from logs and error messages.

### Acceptance criteria

- Admin API never returns full secret values after initial save.

---

## P2-03 — Add PII lifecycle controls

### Evidence

- Conversations, messages, leads, attachment metadata, and integration logs may contain names, phone numbers, locations, and message text.
- Integration logs persist request payloads and response excerpts.

### Required changes

- [ ] Define retention periods by data type.
- [ ] Encrypt sensitive lead and customer fields at rest where appropriate.
- [ ] Redact PII in logs.
- [ ] Add deletion/export workflows.
- [ ] Add scheduled cleanup jobs.

### Acceptance criteria

- Data retention policy is executable, not only documented.

---

## P2-04 — Fix sequential order-number race conditions

### Evidence

- Laban order numbering uses `count + 1` before insert.

### Risk

Concurrent requests can generate duplicate order numbers.

### Required changes

- [ ] Replace `count + 1` with a PostgreSQL sequence or atomic RPC.
- [ ] Apply the same rule to any maintenance numbering path.

### Acceptance criteria

- Concurrent insert test produces unique sequential references.

---

# Phase 3 — Quality Gates and Operations

## P3-01 — Add GitHub Actions CI

### Required checks

- [ ] Python compile check: `python -m compileall actions webhook`.
- [ ] Python lint: Ruff.
- [ ] Unit tests: Pytest.
- [ ] Rasa data validation using generated runtime domain.
- [ ] Rasa E2E smoke tests.
- [ ] Frontend: `pnpm lint`, `pnpm test`, `pnpm build`.
- [ ] Secret scan: Gitleaks or equivalent.
- [ ] Dependency vulnerability scan.
- [ ] Migration syntax validation.

### Acceptance criteria

- Merge is blocked when any required check fails.

---

## P3-02 — Add production smoke tests

### Required paths

- [ ] `/health`
- [ ] `/health/details`
- [ ] `/brands`
- [ ] `/chat`
- [ ] `/uberfix/bot-gateway` allowed action
- [ ] `/uberfix/bot-gateway` rejected action
- [ ] WhatsApp signature rejection
- [ ] Telegram secret rejection
- [ ] Create maintenance request
- [ ] Track maintenance request
- [ ] Draft Daftra invoice and database link

---

## P3-03 — Monitoring, backup, and rollback

### Required changes

- [ ] Structured logs with request IDs.
- [ ] Metrics for errors, latency, queue backlog, Redis health, Rasa health, and OpenAI cost.
- [ ] Alerting for repeated gateway failures.
- [ ] Database backup verification.
- [ ] Model artifact retention and rollback command.
- [ ] Deployment record containing Git SHA and model SHA.

---

# Execution Order

## Release Gate A — Required before public launch

1. P0-01 Privileged UberFix proxy protection.
2. P0-02 Runtime endpoint generation fix.
3. P0-03 Unified systemd root and user.
4. P0-04 Admin RBAC.
5. P0-05 Webhook signature fail-closed behavior.
6. P0-06 Cost endpoint protection.
7. P0-07 Upload hardening.

## Release Gate B — Required before calling the product feature-complete

1. P1-01 Voice ingestion completion.
2. P1-02 KB/upload persistence.
3. P1-03 Durable background queue.
4. P1-04 UberFix action consolidation.

## Release Gate C — Required before normal feature expansion resumes

1. P2 data governance tasks.
2. P3 CI, smoke tests, monitoring, backup, and rollback.

---

# Definition of Done

The project is considered production-closed only when:

- [ ] All P0 items are closed with tests.
- [ ] All active services run the same Git SHA from one canonical path.
- [ ] Rasa validates and trains using generated runtime files.
- [ ] Website text request reaches UberFix gateway and returns a tracking number.
- [ ] WhatsApp text request reaches the same lifecycle.
- [ ] Draft Daftra invoice links back to the maintenance request.
- [ ] Forged webhook and privileged proxy requests are rejected.
- [ ] Uploads are quarantined and not directly public.
- [ ] CI blocks regressions.
- [ ] A rollback command is tested.
