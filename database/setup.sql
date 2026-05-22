-- ══════════════════════════════════════════════════════════════
-- AzaBot v4.0 — Database Setup Script
-- تشغيل: psql -U azabot -d azabot -f database/setup.sql
-- ══════════════════════════════════════════════════════════════

BEGIN;

-- ── Leads (بيانات العملاء المحتملين) ─────────────────────────
CREATE TABLE IF NOT EXISTS leads (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name        text,
    phone       text,
    location    text,
    service_type text,
    brand       text,
    sender_id   text,
    source      text DEFAULT 'chatbot',
    status      text DEFAULT 'new',
    metadata    jsonb NOT NULL DEFAULT '{}',
    created_at  timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS leads_brand_idx ON leads(brand);
CREATE INDEX IF NOT EXISTS leads_status_idx ON leads(status);
CREATE INDEX IF NOT EXISTS leads_created_idx ON leads(created_at DESC);

-- ── Feedback (التقييمات) ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS feedback (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id   text,
    service     text,
    rating      numeric(2,1),
    feedback_text text,
    brand       text,
    created_at  timestamptz NOT NULL DEFAULT now()
);

-- ── Suggestions (الاقتراحات) ──────────────────────────────────
CREATE TABLE IF NOT EXISTS suggestions (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id   text,
    suggestion  text,
    brand       text,
    created_at  timestamptz NOT NULL DEFAULT now()
);

-- ── Escalation Tickets (تذاكر التصعيد) ────────────────────────
CREATE TABLE IF NOT EXISTS escalation_tickets (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id   text,
    reason      text,
    description text,
    brand       text,
    status      text DEFAULT 'open',
    created_at  timestamptz NOT NULL DEFAULT now()
);

-- ── Projects (مشاريع Alazab Construction) ─────────────────────
CREATE TABLE IF NOT EXISTS projects (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id   text,
    project_type text,
    location    text,
    area_size   text,
    description text,
    brand       text DEFAULT 'alazab_construction',
    status      text DEFAULT 'inquiry',
    created_at  timestamptz NOT NULL DEFAULT now()
);

-- ── Laban Orders (طلبات Laban Alasfour) ───────────────────────
CREATE TABLE IF NOT EXISTS laban_orders (
    id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number text UNIQUE,
    client_name  text,
    phone        text,
    unit_type    text,
    material     text,
    dims         text,
    qty          int DEFAULT 1,
    description  text,
    branch       text,
    status       text DEFAULT 'new',
    notes        text,
    created_at   timestamptz NOT NULL DEFAULT now(),
    updated_at   timestamptz
);
CREATE INDEX IF NOT EXISTS laban_orders_status_idx ON laban_orders(status);

COMMIT;

-- ── Verify ────────────────────────────────────────────────────
DO $$
DECLARE
    tbl text;
    tables text[] := ARRAY['leads','feedback','suggestions','escalation_tickets','projects','laban_orders'];
BEGIN
    FOREACH tbl IN ARRAY tables LOOP
        IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = tbl) THEN
            RAISE NOTICE '✅ Table % ready', tbl;
        ELSE
            RAISE WARNING '❌ Table % MISSING', tbl;
        END IF;
    END LOOP;
END $$;
