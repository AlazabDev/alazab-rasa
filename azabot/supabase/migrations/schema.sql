-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.admin_auth (
  id integer NOT NULL CHECK (id = 1),
  password_hash text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT admin_auth_pkey PRIMARY KEY (id)
);
CREATE TABLE public.bot_settings (
  id integer NOT NULL CHECK (id = 1),
  bot_name text NOT NULL DEFAULT 'AzaBot'::text,
  primary_color text NOT NULL DEFAULT '#FFB800'::text,
  welcome_message text NOT NULL DEFAULT 'مرحباً! أنا AzaBot، كيف يمكنني مساعدتك اليوم؟'::text,
  quick_replies jsonb NOT NULL DEFAULT '["ما هي خدماتكم؟", "كيف أتواصل معكم؟", "أريد عرض سعر"]'::jsonb,
  ai_model text NOT NULL DEFAULT 'google/gemini-2.5-flash'::text,
  system_prompt text NOT NULL DEFAULT 'أنت AzaBot، مساعد ذكي ودود يتحدث بالعربية الفصحى السهلة افتراضياً (وبالإنجليزية إذا خاطبك المستخدم بها). كن مختصراً، واضحاً، ومحترفاً.'::text,
  voice_enabled boolean NOT NULL DEFAULT true,
  voice_name text NOT NULL DEFAULT 'ar-SA'::text,
  auto_speak boolean NOT NULL DEFAULT false,
  business_hours_enabled boolean NOT NULL DEFAULT false,
  business_hours jsonb NOT NULL DEFAULT '{"end": "18:00", "days": [0, 1, 2, 3, 4], "start": "09:00", "timezone": "Asia/Riyadh"}'::jsonb,
  offline_message text NOT NULL DEFAULT 'نحن خارج ساعات العمل حالياً. اترك رسالتك وسنرد عليك قريباً.'::text,
  position text NOT NULL DEFAULT 'right'::text CHECK ("position" = ANY (ARRAY['left'::text, 'right'::text])),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  engine text NOT NULL DEFAULT 'lovable'::text CHECK (engine = ANY (ARRAY['lovable'::text, 'rasa'::text])),
  rasa_url text NOT NULL DEFAULT ''::text,
  rasa_timeout_ms integer NOT NULL DEFAULT 15000,
  header_subtitle text NOT NULL DEFAULT 'متصل الآن'::text,
  bubble_style text NOT NULL DEFAULT 'modern'::text,
  show_branding boolean NOT NULL DEFAULT true,
  sound_enabled boolean NOT NULL DEFAULT true,
  allow_human_takeover boolean NOT NULL DEFAULT true,
  avatar_url text NOT NULL DEFAULT ''::text,
  CONSTRAINT bot_settings_pkey PRIMARY KEY (id)
);
CREATE TABLE public.cloud_storage_providers (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  name text NOT NULL,
  provider_type text NOT NULL CHECK (provider_type = ANY (ARRAY['s3'::text, 'oci'::text, 'gcp'::text])),
  bucket_name text NOT NULL,
  region text,
  is_active boolean NOT NULL DEFAULT true,
  config jsonb DEFAULT '{}'::jsonb,
  created_by uuid,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT cloud_storage_providers_pkey PRIMARY KEY (id),
  CONSTRAINT cloud_storage_providers_created_by_fkey FOREIGN KEY (created_by) REFERENCES auth.users(id)
);
CREATE TABLE public.conversations (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  session_id text NOT NULL,
  visitor_name text,
  visitor_email text,
  metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
  status text NOT NULL DEFAULT 'active'::text CHECK (status = ANY (ARRAY['active'::text, 'closed'::text, 'archived'::text])),
  message_count integer NOT NULL DEFAULT 0,
  last_message_at timestamp with time zone NOT NULL DEFAULT now(),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  human_takeover boolean NOT NULL DEFAULT false,
  assigned_admin text,
  admin_notes text,
  CONSTRAINT conversations_pkey PRIMARY KEY (id)
);
CREATE TABLE public.daftra_transactions (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,
  file_id uuid,
  description text NOT NULL,
  amount numeric NOT NULL,
  transaction_type text NOT NULL CHECK (transaction_type = ANY (ARRAY['income'::text, 'expense'::text])),
  category text,
  transaction_date date NOT NULL DEFAULT CURRENT_DATE,
  daftra_reference text,
  status text DEFAULT 'pending'::text CHECK (status = ANY (ARRAY['pending'::text, 'sent'::text, 'confirmed'::text, 'failed'::text])),
  created_by uuid,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT daftra_transactions_pkey PRIMARY KEY (id),
  CONSTRAINT daftra_transactions_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id),
  CONSTRAINT daftra_transactions_file_id_fkey FOREIGN KEY (file_id) REFERENCES public.project_files(id)
);
CREATE TABLE public.file_comments (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  file_id uuid NOT NULL,
  user_id uuid,
  user_name text,
  content text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT file_comments_pkey PRIMARY KEY (id),
  CONSTRAINT file_comments_file_id_fkey FOREIGN KEY (file_id) REFERENCES public.project_files(id)
);
CREATE TABLE public.integrations (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  type text NOT NULL CHECK (type = ANY (ARRAY['webhook'::text, 'telegram'::text, 'whatsapp'::text, 'twilio'::text, 'slack'::text, 'email'::text])),
  name text NOT NULL,
  enabled boolean NOT NULL DEFAULT false,
  config jsonb NOT NULL DEFAULT '{}'::jsonb,
  events jsonb NOT NULL DEFAULT '["message.created", "conversation.started"]'::jsonb,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT integrations_pkey PRIMARY KEY (id)
);
CREATE TABLE public.maintenance_requests (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  ticket_number text NOT NULL DEFAULT ''::text UNIQUE,
  title text NOT NULL,
  description text,
  fault_category USER-DEFINED NOT NULL DEFAULT 'other'::fault_category,
  priority USER-DEFINED NOT NULL DEFAULT 'medium'::maintenance_priority,
  status USER-DEFINED NOT NULL DEFAULT 'new'::maintenance_status,
  building text,
  unit text,
  floor text,
  requester_name text NOT NULL,
  requester_phone text,
  requester_email text,
  source text NOT NULL DEFAULT 'web'::text,
  source_reference text,
  assigned_to uuid,
  assigned_at timestamp with time zone,
  resolution_notes text,
  completed_at timestamp with time zone,
  attachments jsonb DEFAULT '[]'::jsonb,
  created_by uuid,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT maintenance_requests_pkey PRIMARY KEY (id)
);
CREATE TABLE public.messages (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  conversation_id uuid NOT NULL,
  role text NOT NULL CHECK (role = ANY (ARRAY['user'::text, 'assistant'::text, 'system'::text])),
  content text NOT NULL,
  attachments jsonb NOT NULL DEFAULT '[]'::jsonb,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT messages_pkey PRIMARY KEY (id),
  CONSTRAINT messages_conversation_id_fkey FOREIGN KEY (conversation_id) REFERENCES public.conversations(id)
);
CREATE TABLE public.notifications (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  project_id uuid,
  title text NOT NULL,
  message text,
  type text DEFAULT 'info'::text CHECK (type = ANY (ARRAY['info'::text, 'file'::text, 'comment'::text, 'transaction'::text])),
  is_read boolean DEFAULT false,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT notifications_pkey PRIMARY KEY (id),
  CONSTRAINT notifications_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id)
);
CREATE TABLE public.profiles (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL UNIQUE,
  full_name text NOT NULL,
  phone text,
  email text,
  avatar_url text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT profiles_pkey PRIMARY KEY (id)
);
CREATE TABLE public.project_files (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,
  file_name text NOT NULL,
  file_type text NOT NULL CHECK (file_type = ANY (ARRAY['image'::text, 'video'::text, 'audio'::text, 'pdf'::text, 'document'::text, 'other'::text])),
  file_url text NOT NULL,
  thumbnail_url text,
  file_size bigint DEFAULT 0,
  mime_type text,
  duration_seconds integer,
  width integer,
  height integer,
  page_count integer,
  sender_name text,
  sender_phone text,
  whatsapp_message_id text,
  caption text,
  storage_path text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT project_files_pkey PRIMARY KEY (id),
  CONSTRAINT project_files_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id)
);
CREATE TABLE public.project_members (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,
  user_id uuid NOT NULL,
  permission text NOT NULL DEFAULT 'view'::text CHECK (permission = ANY (ARRAY['view'::text, 'download'::text, 'upload'::text, 'edit'::text, 'admin'::text])),
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT project_members_pkey PRIMARY KEY (id),
  CONSTRAINT project_members_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id)
);
CREATE TABLE public.projects (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  project_number text NOT NULL UNIQUE,
  name text NOT NULL,
  client_name text,
  location text,
  description text,
  status text NOT NULL DEFAULT 'active'::text CHECK (status = ANY (ARRAY['active'::text, 'completed'::text, 'archived'::text])),
  thumbnail_url text,
  start_date date,
  created_by uuid,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT projects_pkey PRIMARY KEY (id)
);
CREATE TABLE public.user_roles (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  role USER-DEFINED NOT NULL,
  CONSTRAINT user_roles_pkey PRIMARY KEY (id)
);
CREATE TABLE public.webhook_logs (
  id uuid NOT NULL DEFAULT gen_random_uuid(),
  integration_id uuid,
  integration_type text NOT NULL,
  event text NOT NULL,
  status text NOT NULL CHECK (status = ANY (ARRAY['success'::text, 'failed'::text, 'pending'::text])),
  status_code integer,
  request_payload jsonb,
  response_body text,
  error_message text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT webhook_logs_pkey PRIMARY KEY (id),
  CONSTRAINT webhook_logs_integration_id_fkey FOREIGN KEY (integration_id) REFERENCES public.integrations(id)
);
CREATE TABLE public.whatsapp_integrations (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  user_id uuid,
  business_account_id character varying NOT NULL UNIQUE,
  phone_number_id character varying NOT NULL,
  access_token text NOT NULL,
  status character varying DEFAULT 'active'::character varying,
  created_at timestamp without time zone DEFAULT now(),
  updated_at timestamp without time zone DEFAULT now(),
  expires_at timestamp without time zone,
  CONSTRAINT whatsapp_integrations_pkey PRIMARY KEY (id),
  CONSTRAINT whatsapp_integrations_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id)
);
CREATE TABLE public.whatsapp_media (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  media_id character varying NOT NULL UNIQUE,
  type character varying NOT NULL,
  url text NOT NULL,
  mime_type character varying,
  size bigint,
  caption text,
  uploaded_at timestamp without time zone DEFAULT now(),
  integration_id uuid,
  CONSTRAINT whatsapp_media_pkey PRIMARY KEY (id),
  CONSTRAINT whatsapp_media_integration_id_fkey FOREIGN KEY (integration_id) REFERENCES public.whatsapp_integrations(id)
);
CREATE TABLE public.whatsapp_message_templates (
  template_id text NOT NULL,
  waba_id text NOT NULL,
  waba_name text,
  business_id text,
  business_name text,
  template_name text NOT NULL,
  language text NOT NULL,
  status text CHECK (status IS NULL OR (status = ANY (ARRAY['APPROVED'::text, 'REJECTED'::text, 'PENDING'::text, 'PAUSED'::text, 'DISABLED'::text, 'IN_APPEAL'::text]))),
  category text,
  previous_category text,
  sub_category text,
  parameter_format text,
  library_template_name text,
  namespace text,
  message_send_ttl_seconds integer,
  is_primary_device_delivery_only boolean DEFAULT false,
  body_text text,
  footer_text text,
  header_component jsonb DEFAULT 'null'::jsonb,
  buttons jsonb NOT NULL DEFAULT '[]'::jsonb,
  variables jsonb NOT NULL DEFAULT '{"all": [], "count": 0, "named": [], "positional": []}'::jsonb,
  components jsonb NOT NULL DEFAULT '[]'::jsonb,
  raw_template jsonb NOT NULL,
  source_file text,
  imported_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT whatsapp_message_templates_pkey PRIMARY KEY (template_id)
);
CREATE TABLE public.whatsapp_messages (
  id character varying NOT NULL,
  message text NOT NULL,
  type character varying DEFAULT 'text'::character varying,
  status character varying DEFAULT 'received'::character varying,
  media_url text,
  timestamp timestamp without time zone NOT NULL,
  created_at timestamp without time zone DEFAULT now(),
  integration_id uuid,
  CONSTRAINT whatsapp_messages_pkey PRIMARY KEY (id),
  CONSTRAINT whatsapp_messages_integration_id_fkey FOREIGN KEY (integration_id) REFERENCES public.whatsapp_integrations(id)
);
CREATE TABLE public.whatsapp_templates (
  id uuid NOT NULL DEFAULT uuid_generate_v4(),
  integration_id uuid,
  name character varying NOT NULL,
  template_id character varying,
  body text NOT NULL,
  variables json,
  status character varying DEFAULT 'pending_review'::character varying,
  created_at timestamp without time zone DEFAULT now(),
  CONSTRAINT whatsapp_templates_pkey PRIMARY KEY (id),
  CONSTRAINT whatsapp_templates_integration_id_fkey FOREIGN KEY (integration_id) REFERENCES public.whatsapp_integrations(id)
);