-- ══════════════════════════════════════════════════════════════
-- AzaBot v4 — Missing Tables Migration
-- ══════════════════════════════════════════════════════════════

-- Leads
CREATE TABLE IF NOT EXISTS public.leads (
    id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    brand        text,
    user_name    text,
    user_phone   text,
    user_message text,
    location     text,
    service_type text,
    channel      text DEFAULT 'chatbot',
    source       text DEFAULT 'rasa',
    status       text DEFAULT 'new',
    metadata     jsonb DEFAULT '{}',
    created_at   timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS leads_brand_idx   ON public.leads(brand);
CREATE INDEX IF NOT EXISTS leads_status_idx  ON public.leads(status);
CREATE INDEX IF NOT EXISTS leads_created_idx ON public.leads(created_at DESC);

-- Laban Orders
CREATE TABLE IF NOT EXISTS public.laban_orders (
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
CREATE INDEX IF NOT EXISTS laban_orders_status_idx ON public.laban_orders(status);

-- KB Collections
CREATE TABLE IF NOT EXISTS public.kb_collections (
    id             uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name           text NOT NULL,
    description    text DEFAULT '',
    document_count int DEFAULT 0,
    created_at     timestamptz NOT NULL DEFAULT now()
);

-- KB Documents
CREATE TABLE IF NOT EXISTS public.kb_documents (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    collection_id uuid REFERENCES public.kb_collections(id) ON DELETE CASCADE,
    name          text NOT NULL,
    type          text DEFAULT 'file',
    status        text DEFAULT 'ready',
    metadata      jsonb DEFAULT '{}',
    created_at    timestamptz NOT NULL DEFAULT now()
);

-- WhatsApp Templates
CREATE TABLE IF NOT EXISTS public.whatsapp_templates (
    id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name        text NOT NULL UNIQUE,
    waba_id     text,
    language    text DEFAULT 'ar',
    category    text DEFAULT 'UTILITY',
    components  jsonb DEFAULT '[]',
    status      text DEFAULT 'APPROVED',
    created_at  timestamptz NOT NULL DEFAULT now()
);

-- RLS
ALTER TABLE public.leads            ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.laban_orders     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.kb_collections   ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.kb_documents     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.whatsapp_templates ENABLE ROW LEVEL SECURITY;

-- Policies — بدون IF NOT EXISTS (غير مدعوم في PostgreSQL)
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'service_role_leads' AND tablename = 'leads') THEN
    CREATE POLICY "service_role_leads" ON public.leads FOR ALL TO service_role USING (true);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'service_role_laban' AND tablename = 'laban_orders') THEN
    CREATE POLICY "service_role_laban" ON public.laban_orders FOR ALL TO service_role USING (true);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'service_role_kb_col' AND tablename = 'kb_collections') THEN
    CREATE POLICY "service_role_kb_col" ON public.kb_collections FOR ALL TO service_role USING (true);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'service_role_kb_doc' AND tablename = 'kb_documents') THEN
    CREATE POLICY "service_role_kb_doc" ON public.kb_documents FOR ALL TO service_role USING (true);
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_policies WHERE policyname = 'service_role_wa_tmpl' AND tablename = 'whatsapp_templates') THEN
    CREATE POLICY "service_role_wa_tmpl" ON public.whatsapp_templates FOR ALL TO service_role USING (true);
  END IF;
END $$;
