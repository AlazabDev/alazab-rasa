create extension if not exists "pg_cron" with schema "pg_catalog";

create extension if not exists "hstore" with schema "extensions";

create extension if not exists "hypopg" with schema "extensions";

create extension if not exists "index_advisor" with schema "extensions";

create extension if not exists "pg_prewarm" with schema "extensions";

create extension if not exists "pg_trgm" with schema "extensions";

create extension if not exists "pg_walinspect" with schema "extensions";

create extension if not exists "pgjwt" with schema "extensions";

create extension if not exists "unaccent" with schema "extensions";

create extension if not exists "vector" with schema "extensions";

drop extension if exists "pg_net";

create schema if not exists "pgmq";

create extension if not exists "pgmq" with schema "pgmq";

create schema if not exists "pgtap";

create type "public"."app_role" as enum ('admin', 'architect', 'consultant', 'contractor', 'client', 'viewer');

create type "public"."fault_category" as enum ('electrical', 'plumbing', 'hvac', 'structural', 'painting', 'carpentry', 'cleaning', 'other');

create type "public"."maintenance_priority" as enum ('low', 'medium', 'high', 'urgent');

create type "public"."maintenance_status" as enum ('new', 'assigned', 'in_progress', 'completed', 'cancelled');

revoke delete on table "public"."admin_auth" from "anon";

revoke insert on table "public"."admin_auth" from "anon";

revoke references on table "public"."admin_auth" from "anon";

revoke select on table "public"."admin_auth" from "anon";

revoke trigger on table "public"."admin_auth" from "anon";

revoke truncate on table "public"."admin_auth" from "anon";

revoke update on table "public"."admin_auth" from "anon";

revoke delete on table "public"."admin_auth" from "authenticated";

revoke insert on table "public"."admin_auth" from "authenticated";

revoke references on table "public"."admin_auth" from "authenticated";

revoke select on table "public"."admin_auth" from "authenticated";

revoke trigger on table "public"."admin_auth" from "authenticated";

revoke truncate on table "public"."admin_auth" from "authenticated";

revoke update on table "public"."admin_auth" from "authenticated";

revoke delete on table "public"."bot_settings" from "anon";

revoke insert on table "public"."bot_settings" from "anon";

revoke references on table "public"."bot_settings" from "anon";

revoke select on table "public"."bot_settings" from "anon";

revoke trigger on table "public"."bot_settings" from "anon";

revoke truncate on table "public"."bot_settings" from "anon";

revoke update on table "public"."bot_settings" from "anon";

revoke delete on table "public"."bot_settings" from "authenticated";

revoke insert on table "public"."bot_settings" from "authenticated";

revoke references on table "public"."bot_settings" from "authenticated";

revoke select on table "public"."bot_settings" from "authenticated";

revoke trigger on table "public"."bot_settings" from "authenticated";

revoke truncate on table "public"."bot_settings" from "authenticated";

revoke update on table "public"."bot_settings" from "authenticated";

revoke delete on table "public"."conversations" from "anon";

revoke insert on table "public"."conversations" from "anon";

revoke references on table "public"."conversations" from "anon";

revoke select on table "public"."conversations" from "anon";

revoke trigger on table "public"."conversations" from "anon";

revoke truncate on table "public"."conversations" from "anon";

revoke update on table "public"."conversations" from "anon";

revoke delete on table "public"."conversations" from "authenticated";

revoke insert on table "public"."conversations" from "authenticated";

revoke references on table "public"."conversations" from "authenticated";

revoke select on table "public"."conversations" from "authenticated";

revoke trigger on table "public"."conversations" from "authenticated";

revoke truncate on table "public"."conversations" from "authenticated";

revoke update on table "public"."conversations" from "authenticated";

revoke delete on table "public"."integrations" from "anon";

revoke insert on table "public"."integrations" from "anon";

revoke references on table "public"."integrations" from "anon";

revoke select on table "public"."integrations" from "anon";

revoke trigger on table "public"."integrations" from "anon";

revoke truncate on table "public"."integrations" from "anon";

revoke update on table "public"."integrations" from "anon";

revoke delete on table "public"."integrations" from "authenticated";

revoke insert on table "public"."integrations" from "authenticated";

revoke references on table "public"."integrations" from "authenticated";

revoke select on table "public"."integrations" from "authenticated";

revoke trigger on table "public"."integrations" from "authenticated";

revoke truncate on table "public"."integrations" from "authenticated";

revoke update on table "public"."integrations" from "authenticated";

revoke delete on table "public"."messages" from "anon";

revoke insert on table "public"."messages" from "anon";

revoke references on table "public"."messages" from "anon";

revoke select on table "public"."messages" from "anon";

revoke trigger on table "public"."messages" from "anon";

revoke truncate on table "public"."messages" from "anon";

revoke update on table "public"."messages" from "anon";

revoke delete on table "public"."messages" from "authenticated";

revoke insert on table "public"."messages" from "authenticated";

revoke references on table "public"."messages" from "authenticated";

revoke select on table "public"."messages" from "authenticated";

revoke trigger on table "public"."messages" from "authenticated";

revoke truncate on table "public"."messages" from "authenticated";

revoke update on table "public"."messages" from "authenticated";

revoke delete on table "public"."webhook_logs" from "anon";

revoke insert on table "public"."webhook_logs" from "anon";

revoke references on table "public"."webhook_logs" from "anon";

revoke select on table "public"."webhook_logs" from "anon";

revoke trigger on table "public"."webhook_logs" from "anon";

revoke truncate on table "public"."webhook_logs" from "anon";

revoke update on table "public"."webhook_logs" from "anon";

revoke delete on table "public"."webhook_logs" from "authenticated";

revoke insert on table "public"."webhook_logs" from "authenticated";

revoke references on table "public"."webhook_logs" from "authenticated";

revoke select on table "public"."webhook_logs" from "authenticated";

revoke trigger on table "public"."webhook_logs" from "authenticated";

revoke truncate on table "public"."webhook_logs" from "authenticated";

revoke update on table "public"."webhook_logs" from "authenticated";


  create table "public"."cloud_storage_providers" (
    "id" uuid not null default gen_random_uuid(),
    "name" text not null,
    "provider_type" text not null,
    "bucket_name" text not null,
    "region" text,
    "is_active" boolean not null default true,
    "config" jsonb default '{}'::jsonb,
    "created_by" uuid,
    "created_at" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone not null default now()
      );


alter table "public"."cloud_storage_providers" enable row level security;


  create table "public"."daftra_transactions" (
    "id" uuid not null default gen_random_uuid(),
    "project_id" uuid not null,
    "file_id" uuid,
    "description" text not null,
    "amount" numeric(12,2) not null,
    "transaction_type" text not null,
    "category" text,
    "transaction_date" date not null default CURRENT_DATE,
    "daftra_reference" text,
    "status" text default 'pending'::text,
    "created_by" uuid,
    "created_at" timestamp with time zone not null default now()
      );


alter table "public"."daftra_transactions" enable row level security;


  create table "public"."file_comments" (
    "id" uuid not null default gen_random_uuid(),
    "file_id" uuid not null,
    "user_id" uuid,
    "user_name" text,
    "content" text not null,
    "created_at" timestamp with time zone not null default now()
      );


alter table "public"."file_comments" enable row level security;


  create table "public"."maintenance_requests" (
    "id" uuid not null default gen_random_uuid(),
    "ticket_number" text not null default ''::text,
    "title" text not null,
    "description" text,
    "fault_category" public.fault_category not null default 'other'::public.fault_category,
    "priority" public.maintenance_priority not null default 'medium'::public.maintenance_priority,
    "status" public.maintenance_status not null default 'new'::public.maintenance_status,
    "building" text,
    "unit" text,
    "floor" text,
    "requester_name" text not null,
    "requester_phone" text,
    "requester_email" text,
    "source" text not null default 'web'::text,
    "source_reference" text,
    "assigned_to" uuid,
    "assigned_at" timestamp with time zone,
    "resolution_notes" text,
    "completed_at" timestamp with time zone,
    "attachments" jsonb default '[]'::jsonb,
    "created_by" uuid,
    "created_at" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone not null default now()
      );


alter table "public"."maintenance_requests" enable row level security;


  create table "public"."notifications" (
    "id" uuid not null default gen_random_uuid(),
    "user_id" uuid not null,
    "project_id" uuid,
    "title" text not null,
    "message" text,
    "type" text default 'info'::text,
    "is_read" boolean default false,
    "created_at" timestamp with time zone not null default now()
      );


alter table "public"."notifications" enable row level security;


  create table "public"."profiles" (
    "id" uuid not null default gen_random_uuid(),
    "user_id" uuid not null,
    "full_name" text not null,
    "phone" text,
    "email" text,
    "avatar_url" text,
    "created_at" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone not null default now()
      );


alter table "public"."profiles" enable row level security;


  create table "public"."project_files" (
    "id" uuid not null default gen_random_uuid(),
    "project_id" uuid not null,
    "file_name" text not null,
    "file_type" text not null,
    "file_url" text not null,
    "thumbnail_url" text,
    "file_size" bigint default 0,
    "mime_type" text,
    "duration_seconds" integer,
    "width" integer,
    "height" integer,
    "page_count" integer,
    "sender_name" text,
    "sender_phone" text,
    "whatsapp_message_id" text,
    "caption" text,
    "storage_path" text,
    "created_at" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone not null default now()
      );


alter table "public"."project_files" enable row level security;


  create table "public"."project_members" (
    "id" uuid not null default gen_random_uuid(),
    "project_id" uuid not null,
    "user_id" uuid not null,
    "permission" text not null default 'view'::text,
    "created_at" timestamp with time zone not null default now()
      );


alter table "public"."project_members" enable row level security;


  create table "public"."projects" (
    "id" uuid not null default gen_random_uuid(),
    "project_number" text not null,
    "name" text not null,
    "client_name" text,
    "location" text,
    "description" text,
    "status" text not null default 'active'::text,
    "thumbnail_url" text,
    "start_date" date,
    "created_by" uuid,
    "created_at" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone not null default now()
      );


alter table "public"."projects" enable row level security;


  create table "public"."user_roles" (
    "id" uuid not null default gen_random_uuid(),
    "user_id" uuid not null,
    "role" public.app_role not null
      );


alter table "public"."user_roles" enable row level security;


  create table "public"."whatsapp_integrations" (
    "id" uuid not null default extensions.uuid_generate_v4(),
    "user_id" uuid,
    "business_account_id" character varying(255) not null,
    "phone_number_id" character varying(255) not null,
    "access_token" text not null,
    "status" character varying(50) default 'active'::character varying,
    "created_at" timestamp without time zone default now(),
    "updated_at" timestamp without time zone default now(),
    "expires_at" timestamp without time zone
      );


alter table "public"."whatsapp_integrations" enable row level security;


  create table "public"."whatsapp_media" (
    "id" uuid not null default extensions.uuid_generate_v4(),
    "media_id" character varying(255) not null,
    "type" character varying(50) not null,
    "url" text not null,
    "mime_type" character varying(100),
    "size" bigint,
    "caption" text,
    "uploaded_at" timestamp without time zone default now(),
    "integration_id" uuid
      );


alter table "public"."whatsapp_media" enable row level security;


  create table "public"."whatsapp_message_templates" (
    "template_id" text not null,
    "waba_id" text not null,
    "waba_name" text,
    "business_id" text,
    "business_name" text,
    "template_name" text not null,
    "language" text not null,
    "status" text,
    "category" text,
    "previous_category" text,
    "sub_category" text,
    "parameter_format" text,
    "library_template_name" text,
    "namespace" text,
    "message_send_ttl_seconds" integer,
    "is_primary_device_delivery_only" boolean default false,
    "body_text" text,
    "footer_text" text,
    "header_component" jsonb default 'null'::jsonb,
    "buttons" jsonb not null default '[]'::jsonb,
    "variables" jsonb not null default '{"all": [], "count": 0, "named": [], "positional": []}'::jsonb,
    "components" jsonb not null default '[]'::jsonb,
    "raw_template" jsonb not null,
    "source_file" text,
    "imported_at" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone not null default now()
      );


alter table "public"."whatsapp_message_templates" enable row level security;


  create table "public"."whatsapp_messages" (
    "id" character varying(255) not null,
    "message" text not null,
    "type" character varying(50) default 'text'::character varying,
    "status" character varying(50) default 'received'::character varying,
    "media_url" text,
    "timestamp" timestamp without time zone not null,
    "created_at" timestamp without time zone default now(),
    "integration_id" uuid
      );


alter table "public"."whatsapp_messages" enable row level security;


  create table "public"."whatsapp_templates" (
    "id" uuid not null default extensions.uuid_generate_v4(),
    "integration_id" uuid,
    "name" character varying(255) not null,
    "template_id" character varying(255),
    "body" text not null,
    "variables" json,
    "status" character varying(50) default 'pending_review'::character varying,
    "created_at" timestamp without time zone default now()
      );


alter table "public"."whatsapp_templates" enable row level security;

CREATE UNIQUE INDEX cloud_storage_providers_pkey ON public.cloud_storage_providers USING btree (id);

CREATE UNIQUE INDEX daftra_transactions_pkey ON public.daftra_transactions USING btree (id);

CREATE UNIQUE INDEX file_comments_pkey ON public.file_comments USING btree (id);

CREATE INDEX idx_maintenance_requests_number ON public.maintenance_requests USING btree (ticket_number);

CREATE INDEX ix_whatsapp_templates_category ON public.whatsapp_message_templates USING btree (category);

CREATE INDEX ix_whatsapp_templates_status ON public.whatsapp_message_templates USING btree (status);

CREATE INDEX ix_whatsapp_templates_variables_gin ON public.whatsapp_message_templates USING gin (variables);

CREATE INDEX ix_whatsapp_templates_waba ON public.whatsapp_message_templates USING btree (waba_id);

CREATE UNIQUE INDEX maintenance_requests_pkey ON public.maintenance_requests USING btree (id);

CREATE UNIQUE INDEX maintenance_requests_ticket_number_unique ON public.maintenance_requests USING btree (ticket_number);

CREATE UNIQUE INDEX notifications_pkey ON public.notifications USING btree (id);

CREATE UNIQUE INDEX profiles_pkey ON public.profiles USING btree (id);

CREATE UNIQUE INDEX profiles_user_id_key ON public.profiles USING btree (user_id);

CREATE UNIQUE INDEX project_files_pkey ON public.project_files USING btree (id);

CREATE UNIQUE INDEX project_members_pkey ON public.project_members USING btree (id);

CREATE UNIQUE INDEX project_members_project_id_user_id_key ON public.project_members USING btree (project_id, user_id);

CREATE UNIQUE INDEX projects_pkey ON public.projects USING btree (id);

CREATE UNIQUE INDEX projects_project_number_key ON public.projects USING btree (project_number);

CREATE UNIQUE INDEX user_roles_pkey ON public.user_roles USING btree (id);

CREATE UNIQUE INDEX user_roles_user_id_role_key ON public.user_roles USING btree (user_id, role);

CREATE UNIQUE INDEX ux_whatsapp_templates_waba_name_lang ON public.whatsapp_message_templates USING btree (waba_id, template_name, language);

CREATE UNIQUE INDEX whatsapp_integrations_business_account_id_key ON public.whatsapp_integrations USING btree (business_account_id);

CREATE UNIQUE INDEX whatsapp_integrations_pkey ON public.whatsapp_integrations USING btree (id);

CREATE UNIQUE INDEX whatsapp_media_media_id_key ON public.whatsapp_media USING btree (media_id);

CREATE UNIQUE INDEX whatsapp_media_pkey ON public.whatsapp_media USING btree (id);

CREATE UNIQUE INDEX whatsapp_message_templates_pkey ON public.whatsapp_message_templates USING btree (template_id);

CREATE UNIQUE INDEX whatsapp_messages_pkey ON public.whatsapp_messages USING btree (id);

CREATE UNIQUE INDEX whatsapp_templates_pkey ON public.whatsapp_templates USING btree (id);

alter table "public"."cloud_storage_providers" add constraint "cloud_storage_providers_pkey" PRIMARY KEY using index "cloud_storage_providers_pkey";

alter table "public"."daftra_transactions" add constraint "daftra_transactions_pkey" PRIMARY KEY using index "daftra_transactions_pkey";

alter table "public"."file_comments" add constraint "file_comments_pkey" PRIMARY KEY using index "file_comments_pkey";

alter table "public"."maintenance_requests" add constraint "maintenance_requests_pkey" PRIMARY KEY using index "maintenance_requests_pkey";

alter table "public"."notifications" add constraint "notifications_pkey" PRIMARY KEY using index "notifications_pkey";

alter table "public"."profiles" add constraint "profiles_pkey" PRIMARY KEY using index "profiles_pkey";

alter table "public"."project_files" add constraint "project_files_pkey" PRIMARY KEY using index "project_files_pkey";

alter table "public"."project_members" add constraint "project_members_pkey" PRIMARY KEY using index "project_members_pkey";

alter table "public"."projects" add constraint "projects_pkey" PRIMARY KEY using index "projects_pkey";

alter table "public"."user_roles" add constraint "user_roles_pkey" PRIMARY KEY using index "user_roles_pkey";

alter table "public"."whatsapp_integrations" add constraint "whatsapp_integrations_pkey" PRIMARY KEY using index "whatsapp_integrations_pkey";

alter table "public"."whatsapp_media" add constraint "whatsapp_media_pkey" PRIMARY KEY using index "whatsapp_media_pkey";

alter table "public"."whatsapp_message_templates" add constraint "whatsapp_message_templates_pkey" PRIMARY KEY using index "whatsapp_message_templates_pkey";

alter table "public"."whatsapp_messages" add constraint "whatsapp_messages_pkey" PRIMARY KEY using index "whatsapp_messages_pkey";

alter table "public"."whatsapp_templates" add constraint "whatsapp_templates_pkey" PRIMARY KEY using index "whatsapp_templates_pkey";

alter table "public"."cloud_storage_providers" add constraint "cloud_storage_providers_created_by_fkey" FOREIGN KEY (created_by) REFERENCES auth.users(id) not valid;

alter table "public"."cloud_storage_providers" validate constraint "cloud_storage_providers_created_by_fkey";

alter table "public"."cloud_storage_providers" add constraint "cloud_storage_providers_provider_type_check" CHECK ((provider_type = ANY (ARRAY['s3'::text, 'oci'::text, 'gcp'::text]))) not valid;

alter table "public"."cloud_storage_providers" validate constraint "cloud_storage_providers_provider_type_check";

alter table "public"."daftra_transactions" add constraint "daftra_transactions_file_id_fkey" FOREIGN KEY (file_id) REFERENCES public.project_files(id) ON DELETE SET NULL not valid;

alter table "public"."daftra_transactions" validate constraint "daftra_transactions_file_id_fkey";

alter table "public"."daftra_transactions" add constraint "daftra_transactions_project_id_fkey" FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE not valid;

alter table "public"."daftra_transactions" validate constraint "daftra_transactions_project_id_fkey";

alter table "public"."daftra_transactions" add constraint "daftra_transactions_status_check" CHECK ((status = ANY (ARRAY['pending'::text, 'sent'::text, 'confirmed'::text, 'failed'::text]))) not valid;

alter table "public"."daftra_transactions" validate constraint "daftra_transactions_status_check";

alter table "public"."daftra_transactions" add constraint "daftra_transactions_transaction_type_check" CHECK ((transaction_type = ANY (ARRAY['income'::text, 'expense'::text]))) not valid;

alter table "public"."daftra_transactions" validate constraint "daftra_transactions_transaction_type_check";

alter table "public"."file_comments" add constraint "file_comments_file_id_fkey" FOREIGN KEY (file_id) REFERENCES public.project_files(id) ON DELETE CASCADE not valid;

alter table "public"."file_comments" validate constraint "file_comments_file_id_fkey";

alter table "public"."maintenance_requests" add constraint "maintenance_requests_ticket_number_unique" UNIQUE using index "maintenance_requests_ticket_number_unique";

alter table "public"."notifications" add constraint "notifications_project_id_fkey" FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE not valid;

alter table "public"."notifications" validate constraint "notifications_project_id_fkey";

alter table "public"."notifications" add constraint "notifications_type_check" CHECK ((type = ANY (ARRAY['info'::text, 'file'::text, 'comment'::text, 'transaction'::text]))) not valid;

alter table "public"."notifications" validate constraint "notifications_type_check";

alter table "public"."profiles" add constraint "profiles_user_id_key" UNIQUE using index "profiles_user_id_key";

alter table "public"."project_files" add constraint "project_files_file_type_check" CHECK ((file_type = ANY (ARRAY['image'::text, 'video'::text, 'audio'::text, 'pdf'::text, 'document'::text, 'other'::text]))) not valid;

alter table "public"."project_files" validate constraint "project_files_file_type_check";

alter table "public"."project_files" add constraint "project_files_project_id_fkey" FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE not valid;

alter table "public"."project_files" validate constraint "project_files_project_id_fkey";

alter table "public"."project_members" add constraint "project_members_permission_check" CHECK ((permission = ANY (ARRAY['view'::text, 'download'::text, 'upload'::text, 'edit'::text, 'admin'::text]))) not valid;

alter table "public"."project_members" validate constraint "project_members_permission_check";

alter table "public"."project_members" add constraint "project_members_project_id_fkey" FOREIGN KEY (project_id) REFERENCES public.projects(id) ON DELETE CASCADE not valid;

alter table "public"."project_members" validate constraint "project_members_project_id_fkey";

alter table "public"."project_members" add constraint "project_members_project_id_user_id_key" UNIQUE using index "project_members_project_id_user_id_key";

alter table "public"."projects" add constraint "projects_project_number_key" UNIQUE using index "projects_project_number_key";

alter table "public"."projects" add constraint "projects_status_check" CHECK ((status = ANY (ARRAY['active'::text, 'completed'::text, 'archived'::text]))) not valid;

alter table "public"."projects" validate constraint "projects_status_check";

alter table "public"."user_roles" add constraint "user_roles_user_id_role_key" UNIQUE using index "user_roles_user_id_role_key";

alter table "public"."whatsapp_integrations" add constraint "whatsapp_integrations_business_account_id_key" UNIQUE using index "whatsapp_integrations_business_account_id_key";

alter table "public"."whatsapp_integrations" add constraint "whatsapp_integrations_user_id_fkey" FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE not valid;

alter table "public"."whatsapp_integrations" validate constraint "whatsapp_integrations_user_id_fkey";

alter table "public"."whatsapp_media" add constraint "whatsapp_media_integration_id_fkey" FOREIGN KEY (integration_id) REFERENCES public.whatsapp_integrations(id) not valid;

alter table "public"."whatsapp_media" validate constraint "whatsapp_media_integration_id_fkey";

alter table "public"."whatsapp_media" add constraint "whatsapp_media_media_id_key" UNIQUE using index "whatsapp_media_media_id_key";

alter table "public"."whatsapp_message_templates" add constraint "whatsapp_message_templates_status_chk" CHECK (((status IS NULL) OR (status = ANY (ARRAY['APPROVED'::text, 'REJECTED'::text, 'PENDING'::text, 'PAUSED'::text, 'DISABLED'::text, 'IN_APPEAL'::text])))) not valid;

alter table "public"."whatsapp_message_templates" validate constraint "whatsapp_message_templates_status_chk";

alter table "public"."whatsapp_messages" add constraint "whatsapp_messages_integration_id_fkey" FOREIGN KEY (integration_id) REFERENCES public.whatsapp_integrations(id) ON DELETE CASCADE not valid;

alter table "public"."whatsapp_messages" validate constraint "whatsapp_messages_integration_id_fkey";

alter table "public"."whatsapp_templates" add constraint "whatsapp_templates_integration_id_fkey" FOREIGN KEY (integration_id) REFERENCES public.whatsapp_integrations(id) ON DELETE CASCADE not valid;

alter table "public"."whatsapp_templates" validate constraint "whatsapp_templates_integration_id_fkey";

set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.generate_ticket_number()
 RETURNS trigger
 LANGUAGE plpgsql
 SET search_path TO 'public'
AS $function$
DECLARE
  seq_num integer;
BEGIN
  SELECT COALESCE(MAX(CAST(SUBSTRING(ticket_number FROM 'MNT-\d{4}-(\d+)') AS integer)), 0) + 1
  INTO seq_num
  FROM public.maintenance_requests
  WHERE ticket_number LIKE 'MNT-' || to_char(now(), 'YYYY') || '-%';
  
  NEW.ticket_number := 'MNT-' || to_char(now(), 'YYYY') || '-' || LPAD(seq_num::text, 4, '0');
  RETURN NEW;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.get_daily_message_counts(days integer DEFAULT 7)
 RETURNS TABLE(date text, count bigint)
 LANGUAGE plpgsql
 SET search_path TO 'public', 'auth'
AS $function$
BEGIN
  RETURN QUERY
  SELECT
    TO_CHAR(DATE_TRUNC('day', created_at), 'YYYY-MM-DD') as date,
    COUNT(*) as count
  FROM whatsapp_messages
  WHERE created_at >= NOW() - INTERVAL '1 day' * days
  GROUP BY DATE_TRUNC('day', created_at)
  ORDER BY date DESC;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.get_message_status_counts()
 RETURNS TABLE(sent bigint, delivered bigint, read bigint, failed bigint)
 LANGUAGE plpgsql
 SET search_path TO 'public', 'auth'
AS $function$
BEGIN
  RETURN QUERY
  SELECT
    COUNT(*) FILTER (WHERE status = 'sent'),
    COUNT(*) FILTER (WHERE status = 'delivered'),
    COUNT(*) FILTER (WHERE status = 'read'),
    COUNT(*) FILTER (WHERE status = 'failed')
  FROM whatsapp_messages;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.handle_new_user()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public', 'auth'
AS $function$
BEGIN
  INSERT INTO public.profiles (user_id, full_name, email)
  VALUES (NEW.id, COALESCE(NEW.raw_user_meta_data->>'full_name', 'مستخدم جديد'), NEW.email);
  RETURN NEW;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.has_role(_user_id uuid, _role public.app_role)
 RETURNS boolean
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public', 'auth'
AS $function$
  SELECT EXISTS (SELECT 1 FROM public.user_roles WHERE user_id = _user_id AND role = _role)
$function$
;

CREATE OR REPLACE FUNCTION public.rls_auto_enable()
 RETURNS event_trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public', 'auth'
AS $function$
DECLARE
  cmd record;
BEGIN
  FOR cmd IN
    SELECT *
    FROM pg_event_trigger_ddl_commands()
    WHERE command_tag IN ('CREATE TABLE', 'CREATE TABLE AS', 'SELECT INTO')
      AND object_type IN ('table','partitioned table')
  LOOP
     IF cmd.schema_name IS NOT NULL AND cmd.schema_name IN ('public') AND cmd.schema_name NOT IN ('pg_catalog','information_schema') AND cmd.schema_name NOT LIKE 'pg_toast%' AND cmd.schema_name NOT LIKE 'pg_temp%' THEN
      BEGIN
        EXECUTE format('alter table if exists %s enable row level security', cmd.object_identity);
        RAISE LOG 'rls_auto_enable: enabled RLS on %', cmd.object_identity;
      EXCEPTION
        WHEN OTHERS THEN
          RAISE LOG 'rls_auto_enable: failed to enable RLS on %', cmd.object_identity;
      END;
     ELSE
        RAISE LOG 'rls_auto_enable: skip % (either system schema or not in enforced list: %.)', cmd.object_identity, cmd.schema_name;
     END IF;
  END LOOP;
END;
$function$
;

CREATE OR REPLACE FUNCTION public.update_updated_at_column()
 RETURNS trigger
 LANGUAGE plpgsql
 SET search_path TO 'public'
AS $function$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$function$
;

create or replace view "public"."v_whatsapp_message_templates" as  SELECT template_id,
    waba_id,
    waba_name,
    template_name,
    language,
    status,
    category,
    parameter_format,
    body_text,
    footer_text,
    jsonb_array_length(buttons) AS buttons_count,
    COALESCE(((variables ->> 'count'::text))::integer, 0) AS variables_count,
    (variables -> 'all'::text) AS variables_all,
    imported_at,
    updated_at
   FROM public.whatsapp_message_templates;


grant delete on table "public"."cloud_storage_providers" to "service_role";

grant insert on table "public"."cloud_storage_providers" to "service_role";

grant references on table "public"."cloud_storage_providers" to "service_role";

grant select on table "public"."cloud_storage_providers" to "service_role";

grant trigger on table "public"."cloud_storage_providers" to "service_role";

grant truncate on table "public"."cloud_storage_providers" to "service_role";

grant update on table "public"."cloud_storage_providers" to "service_role";

grant delete on table "public"."daftra_transactions" to "service_role";

grant insert on table "public"."daftra_transactions" to "service_role";

grant references on table "public"."daftra_transactions" to "service_role";

grant select on table "public"."daftra_transactions" to "service_role";

grant trigger on table "public"."daftra_transactions" to "service_role";

grant truncate on table "public"."daftra_transactions" to "service_role";

grant update on table "public"."daftra_transactions" to "service_role";

grant delete on table "public"."file_comments" to "service_role";

grant insert on table "public"."file_comments" to "service_role";

grant references on table "public"."file_comments" to "service_role";

grant select on table "public"."file_comments" to "service_role";

grant trigger on table "public"."file_comments" to "service_role";

grant truncate on table "public"."file_comments" to "service_role";

grant update on table "public"."file_comments" to "service_role";

grant delete on table "public"."maintenance_requests" to "service_role";

grant insert on table "public"."maintenance_requests" to "service_role";

grant references on table "public"."maintenance_requests" to "service_role";

grant select on table "public"."maintenance_requests" to "service_role";

grant trigger on table "public"."maintenance_requests" to "service_role";

grant truncate on table "public"."maintenance_requests" to "service_role";

grant update on table "public"."maintenance_requests" to "service_role";

grant delete on table "public"."notifications" to "service_role";

grant insert on table "public"."notifications" to "service_role";

grant references on table "public"."notifications" to "service_role";

grant select on table "public"."notifications" to "service_role";

grant trigger on table "public"."notifications" to "service_role";

grant truncate on table "public"."notifications" to "service_role";

grant update on table "public"."notifications" to "service_role";

grant delete on table "public"."profiles" to "service_role";

grant insert on table "public"."profiles" to "service_role";

grant references on table "public"."profiles" to "service_role";

grant select on table "public"."profiles" to "service_role";

grant trigger on table "public"."profiles" to "service_role";

grant truncate on table "public"."profiles" to "service_role";

grant update on table "public"."profiles" to "service_role";

grant delete on table "public"."project_files" to "service_role";

grant insert on table "public"."project_files" to "service_role";

grant references on table "public"."project_files" to "service_role";

grant select on table "public"."project_files" to "service_role";

grant trigger on table "public"."project_files" to "service_role";

grant truncate on table "public"."project_files" to "service_role";

grant update on table "public"."project_files" to "service_role";

grant delete on table "public"."project_members" to "service_role";

grant insert on table "public"."project_members" to "service_role";

grant references on table "public"."project_members" to "service_role";

grant select on table "public"."project_members" to "service_role";

grant trigger on table "public"."project_members" to "service_role";

grant truncate on table "public"."project_members" to "service_role";

grant update on table "public"."project_members" to "service_role";

grant delete on table "public"."projects" to "service_role";

grant insert on table "public"."projects" to "service_role";

grant references on table "public"."projects" to "service_role";

grant select on table "public"."projects" to "service_role";

grant trigger on table "public"."projects" to "service_role";

grant truncate on table "public"."projects" to "service_role";

grant update on table "public"."projects" to "service_role";

grant delete on table "public"."user_roles" to "service_role";

grant insert on table "public"."user_roles" to "service_role";

grant references on table "public"."user_roles" to "service_role";

grant select on table "public"."user_roles" to "service_role";

grant trigger on table "public"."user_roles" to "service_role";

grant truncate on table "public"."user_roles" to "service_role";

grant update on table "public"."user_roles" to "service_role";

grant delete on table "public"."whatsapp_integrations" to "service_role";

grant insert on table "public"."whatsapp_integrations" to "service_role";

grant references on table "public"."whatsapp_integrations" to "service_role";

grant select on table "public"."whatsapp_integrations" to "service_role";

grant trigger on table "public"."whatsapp_integrations" to "service_role";

grant truncate on table "public"."whatsapp_integrations" to "service_role";

grant update on table "public"."whatsapp_integrations" to "service_role";

grant delete on table "public"."whatsapp_media" to "service_role";

grant insert on table "public"."whatsapp_media" to "service_role";

grant references on table "public"."whatsapp_media" to "service_role";

grant select on table "public"."whatsapp_media" to "service_role";

grant trigger on table "public"."whatsapp_media" to "service_role";

grant truncate on table "public"."whatsapp_media" to "service_role";

grant update on table "public"."whatsapp_media" to "service_role";

grant delete on table "public"."whatsapp_message_templates" to "service_role";

grant insert on table "public"."whatsapp_message_templates" to "service_role";

grant references on table "public"."whatsapp_message_templates" to "service_role";

grant select on table "public"."whatsapp_message_templates" to "service_role";

grant trigger on table "public"."whatsapp_message_templates" to "service_role";

grant truncate on table "public"."whatsapp_message_templates" to "service_role";

grant update on table "public"."whatsapp_message_templates" to "service_role";

grant delete on table "public"."whatsapp_messages" to "service_role";

grant insert on table "public"."whatsapp_messages" to "service_role";

grant references on table "public"."whatsapp_messages" to "service_role";

grant select on table "public"."whatsapp_messages" to "service_role";

grant trigger on table "public"."whatsapp_messages" to "service_role";

grant truncate on table "public"."whatsapp_messages" to "service_role";

grant update on table "public"."whatsapp_messages" to "service_role";

grant delete on table "public"."whatsapp_templates" to "service_role";

grant insert on table "public"."whatsapp_templates" to "service_role";

grant references on table "public"."whatsapp_templates" to "service_role";

grant select on table "public"."whatsapp_templates" to "service_role";

grant trigger on table "public"."whatsapp_templates" to "service_role";

grant truncate on table "public"."whatsapp_templates" to "service_role";

grant update on table "public"."whatsapp_templates" to "service_role";


  create policy "deny_direct_client_access_admin_auth"
  on "public"."admin_auth"
  as permissive
  for select
  to anon, authenticated
using (false);



  create policy "Admins manage cloud storage providers"
  on "public"."cloud_storage_providers"
  as permissive
  for all
  to public
using (public.has_role(auth.uid(), 'admin'::public.app_role));



  create policy "deny_direct_client_access_conversations"
  on "public"."conversations"
  as permissive
  for select
  to anon, authenticated
using (false);



  create policy "Admins manage transactions"
  on "public"."daftra_transactions"
  as permissive
  for all
  to public
using (public.has_role(auth.uid(), 'admin'::public.app_role));



  create policy "Members view project transactions"
  on "public"."daftra_transactions"
  as permissive
  for select
  to public
using ((EXISTS ( SELECT 1
   FROM public.project_members
  WHERE ((project_members.project_id = daftra_transactions.project_id) AND (project_members.user_id = auth.uid())))));



  create policy "Authenticated users add comments"
  on "public"."file_comments"
  as permissive
  for insert
  to public
with check ((auth.uid() IS NOT NULL));



  create policy "View comments on accessible files"
  on "public"."file_comments"
  as permissive
  for select
  to public
using (((EXISTS ( SELECT 1
   FROM (public.project_files pf
     JOIN public.project_members pm ON ((pm.project_id = pf.project_id)))
  WHERE ((pf.id = file_comments.file_id) AND (pm.user_id = auth.uid())))) OR public.has_role(auth.uid(), 'admin'::public.app_role)));



  create policy "deny_direct_client_access_integrations"
  on "public"."integrations"
  as permissive
  for select
  to anon, authenticated
using (false);



  create policy "API gateway inserts"
  on "public"."maintenance_requests"
  as permissive
  for insert
  to anon
with check ((source = ANY (ARRAY['whatsapp'::text, 'erp'::text, 'app'::text, 'form'::text])));



  create policy "Admins manage all maintenance requests"
  on "public"."maintenance_requests"
  as permissive
  for all
  to public
using (public.has_role(auth.uid(), 'admin'::public.app_role));



  create policy "Assigned users update maintenance requests"
  on "public"."maintenance_requests"
  as permissive
  for update
  to authenticated
using ((assigned_to = auth.uid()));



  create policy "Authenticated users create maintenance requests"
  on "public"."maintenance_requests"
  as permissive
  for insert
  to authenticated
with check ((auth.uid() IS NOT NULL));



  create policy "Public ticket lookup"
  on "public"."maintenance_requests"
  as permissive
  for select
  to anon
using (true);



  create policy "Users view own maintenance requests"
  on "public"."maintenance_requests"
  as permissive
  for select
  to authenticated
using (((created_by = auth.uid()) OR (assigned_to = auth.uid())));



  create policy "deny_direct_client_access_messages"
  on "public"."messages"
  as permissive
  for select
  to anon, authenticated
using (false);



  create policy "Authenticated insert notifications"
  on "public"."notifications"
  as permissive
  for insert
  to public
with check ((auth.uid() IS NOT NULL));



  create policy "Users update own notifications"
  on "public"."notifications"
  as permissive
  for update
  to public
using ((user_id = auth.uid()));



  create policy "Users view own notifications"
  on "public"."notifications"
  as permissive
  for select
  to public
using ((user_id = auth.uid()));



  create policy "Users can insert own profile"
  on "public"."profiles"
  as permissive
  for insert
  to public
with check ((auth.uid() = user_id));



  create policy "Users can update own profile"
  on "public"."profiles"
  as permissive
  for update
  to public
using ((auth.uid() = user_id));



  create policy "Users can view all profiles"
  on "public"."profiles"
  as permissive
  for select
  to public
using (true);



  create policy "Admins manage all files"
  on "public"."project_files"
  as permissive
  for all
  to public
using (public.has_role(auth.uid(), 'admin'::public.app_role));



  create policy "Authenticated insert files"
  on "public"."project_files"
  as permissive
  for insert
  to public
with check ((auth.uid() IS NOT NULL));



  create policy "Creators view own project files"
  on "public"."project_files"
  as permissive
  for select
  to authenticated
using ((EXISTS ( SELECT 1
   FROM public.projects
  WHERE ((projects.id = project_files.project_id) AND (projects.created_by = auth.uid())))));



  create policy "Members view project files"
  on "public"."project_files"
  as permissive
  for select
  to public
using ((EXISTS ( SELECT 1
   FROM public.project_members
  WHERE ((project_members.project_id = project_files.project_id) AND (project_members.user_id = auth.uid())))));



  create policy "Admins manage project members"
  on "public"."project_members"
  as permissive
  for all
  to public
using (public.has_role(auth.uid(), 'admin'::public.app_role));



  create policy "Members view own memberships"
  on "public"."project_members"
  as permissive
  for select
  to public
using ((user_id = auth.uid()));



  create policy "Admins can do everything on projects"
  on "public"."projects"
  as permissive
  for all
  to public
using (public.has_role(auth.uid(), 'admin'::public.app_role));



  create policy "Authenticated users can insert projects"
  on "public"."projects"
  as permissive
  for insert
  to authenticated
with check ((auth.uid() IS NOT NULL));



  create policy "Authenticated users can update own projects"
  on "public"."projects"
  as permissive
  for update
  to authenticated
using ((created_by = auth.uid()));



  create policy "Creators can view own projects"
  on "public"."projects"
  as permissive
  for select
  to authenticated
using ((created_by = auth.uid()));



  create policy "Members can view their projects"
  on "public"."projects"
  as permissive
  for select
  to public
using ((EXISTS ( SELECT 1
   FROM public.project_members
  WHERE ((project_members.project_id = projects.id) AND (project_members.user_id = auth.uid())))));



  create policy "Admins manage roles"
  on "public"."user_roles"
  as permissive
  for all
  to public
using (public.has_role(auth.uid(), 'admin'::public.app_role));



  create policy "Users view own roles"
  on "public"."user_roles"
  as permissive
  for select
  to public
using ((user_id = auth.uid()));



  create policy "deny_direct_client_access_webhook_logs"
  on "public"."webhook_logs"
  as permissive
  for select
  to anon, authenticated
using (false);



  create policy "Users can view their integrations"
  on "public"."whatsapp_integrations"
  as permissive
  for select
  to public
using ((auth.uid() = user_id));



  create policy "deny_direct_client_access_whatsapp_media"
  on "public"."whatsapp_media"
  as permissive
  for select
  to anon, authenticated
using (false);



  create policy "deny_direct_client_access_whatsapp_message_templates"
  on "public"."whatsapp_message_templates"
  as permissive
  for select
  to anon, authenticated
using (false);



  create policy "Users can view their messages"
  on "public"."whatsapp_messages"
  as permissive
  for select
  to public
using ((integration_id IN ( SELECT whatsapp_integrations.id
   FROM public.whatsapp_integrations
  WHERE (whatsapp_integrations.user_id = auth.uid()))));



  create policy "deny_direct_client_access_whatsapp_templates"
  on "public"."whatsapp_templates"
  as permissive
  for select
  to anon, authenticated
using (false);


CREATE TRIGGER update_cloud_storage_providers_updated_at BEFORE UPDATE ON public.cloud_storage_providers FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER set_ticket_number BEFORE INSERT ON public.maintenance_requests FOR EACH ROW WHEN (((new.ticket_number IS NULL) OR (new.ticket_number = ''::text))) EXECUTE FUNCTION public.generate_ticket_number();

CREATE TRIGGER update_maintenance_requests_updated_at BEFORE UPDATE ON public.maintenance_requests FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_project_files_updated_at BEFORE UPDATE ON public.project_files FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON public.projects FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER on_auth_user_created AFTER INSERT ON auth.users FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();


  create policy "Admins delete files"
  on "storage"."objects"
  as permissive
  for delete
  to public
using (((bucket_id = 'project-files'::text) AND public.has_role(auth.uid(), 'admin'::public.app_role)));



  create policy "Authenticated users upload files"
  on "storage"."objects"
  as permissive
  for insert
  to public
with check ((bucket_id = 'project-files'::text));



