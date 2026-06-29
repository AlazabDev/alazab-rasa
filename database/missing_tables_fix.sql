-- Additional tables for AzaBot CRM and Feedback systems
-- Syncing with action_general.py logic

BEGIN;

CREATE TABLE IF NOT EXISTS leads (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text,
    phone text,
    location text,
    service_type text,
    brand text,
    sender_id text,
    source text DEFAULT 'chatbot',
    status text DEFAULT 'new',
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb, -- Store dynamic lead info (budget, urgency, etc.)
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS feedback (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id text,
    service text,
    rating numeric(2,1),
    feedback_text text,
    brand text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS suggestions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id text,
    suggestion text,
    brand text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS escalation_tickets (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id text,
    details text,
    brand text,
    priority text DEFAULT 'high',
    status text DEFAULT 'open',
    assigned_to text, -- Name or ID of the human agent
    created_at timestamptz NOT NULL DEFAULT now()
);

-- Production Project Tracking (For Construction and Finishing)
CREATE TABLE IF NOT EXISTS projects (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_number text UNIQUE,
    client_name text,
    client_phone text,
    brand text, -- 'alazab', 'luxury', 'brand_identity'
    project_type text, -- 'construction', 'finishing', 'fitout'
    status text DEFAULT 'planning',
    progress_percentage integer DEFAULT 0,
    daftra_client_id text,
    total_budget numeric(15,2),
    paid_amount numeric(15,2) DEFAULT 0,
    metadata jsonb DEFAULT '{}'::jsonb,
    start_date date,
    end_date date,
    created_at timestamptz NOT NULL DEFAULT now()
);

-- Integrate Daftra Accounting Columns into Maintenance System
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='maintenance_requests' AND column_name='daftra_client_id') THEN
        ALTER TABLE maintenance_requests ADD COLUMN daftra_client_id text;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='maintenance_requests' AND column_name='daftra_invoice_id') THEN
        ALTER TABLE maintenance_requests ADD COLUMN daftra_invoice_id text;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='maintenance_requests' AND column_name='daftra_invoice_number') THEN
        ALTER TABLE maintenance_requests ADD COLUMN daftra_invoice_number text;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='maintenance_requests' AND column_name='daftra_document_url') THEN
        ALTER TABLE maintenance_requests ADD COLUMN daftra_document_url text;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='maintenance_requests' AND column_name='payment_status') THEN
        ALTER TABLE maintenance_requests ADD COLUMN payment_status text DEFAULT 'unpaid';
    END IF;
END $$;

COMMIT;
