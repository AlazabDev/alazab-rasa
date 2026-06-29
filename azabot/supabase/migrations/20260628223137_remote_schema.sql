create sequence "public"."events_id_seq";

create sequence "public"."maintenance_request_number_seq";

create sequence "public"."whatsapp_templates_id_seq";

drop policy "service_role_kb_col" on "public"."kb_collections";

drop policy "service_role_kb_doc" on "public"."kb_documents";

drop policy "service_role_laban" on "public"."laban_orders";

drop policy "service_role_leads" on "public"."leads";

drop policy "deny_direct_client_access_whatsapp_templates" on "public"."whatsapp_templates";

drop policy "service_role_wa_tmpl" on "public"."whatsapp_templates";

revoke delete on table "public"."cloud_storage_providers" from "anon";

revoke insert on table "public"."cloud_storage_providers" from "anon";

revoke references on table "public"."cloud_storage_providers" from "anon";

revoke select on table "public"."cloud_storage_providers" from "anon";

revoke trigger on table "public"."cloud_storage_providers" from "anon";

revoke truncate on table "public"."cloud_storage_providers" from "anon";

revoke update on table "public"."cloud_storage_providers" from "anon";

revoke delete on table "public"."cloud_storage_providers" from "authenticated";

revoke insert on table "public"."cloud_storage_providers" from "authenticated";

revoke references on table "public"."cloud_storage_providers" from "authenticated";

revoke select on table "public"."cloud_storage_providers" from "authenticated";

revoke trigger on table "public"."cloud_storage_providers" from "authenticated";

revoke truncate on table "public"."cloud_storage_providers" from "authenticated";

revoke update on table "public"."cloud_storage_providers" from "authenticated";

revoke delete on table "public"."daftra_transactions" from "anon";

revoke insert on table "public"."daftra_transactions" from "anon";

revoke references on table "public"."daftra_transactions" from "anon";

revoke select on table "public"."daftra_transactions" from "anon";

revoke trigger on table "public"."daftra_transactions" from "anon";

revoke truncate on table "public"."daftra_transactions" from "anon";

revoke update on table "public"."daftra_transactions" from "anon";

revoke delete on table "public"."daftra_transactions" from "authenticated";

revoke insert on table "public"."daftra_transactions" from "authenticated";

revoke references on table "public"."daftra_transactions" from "authenticated";

revoke select on table "public"."daftra_transactions" from "authenticated";

revoke trigger on table "public"."daftra_transactions" from "authenticated";

revoke truncate on table "public"."daftra_transactions" from "authenticated";

revoke update on table "public"."daftra_transactions" from "authenticated";

revoke delete on table "public"."file_comments" from "anon";

revoke insert on table "public"."file_comments" from "anon";

revoke references on table "public"."file_comments" from "anon";

revoke select on table "public"."file_comments" from "anon";

revoke trigger on table "public"."file_comments" from "anon";

revoke truncate on table "public"."file_comments" from "anon";

revoke update on table "public"."file_comments" from "anon";

revoke delete on table "public"."file_comments" from "authenticated";

revoke insert on table "public"."file_comments" from "authenticated";

revoke references on table "public"."file_comments" from "authenticated";

revoke select on table "public"."file_comments" from "authenticated";

revoke trigger on table "public"."file_comments" from "authenticated";

revoke truncate on table "public"."file_comments" from "authenticated";

revoke update on table "public"."file_comments" from "authenticated";

revoke delete on table "public"."kb_collections" from "anon";

revoke insert on table "public"."kb_collections" from "anon";

revoke references on table "public"."kb_collections" from "anon";

revoke select on table "public"."kb_collections" from "anon";

revoke trigger on table "public"."kb_collections" from "anon";

revoke truncate on table "public"."kb_collections" from "anon";

revoke update on table "public"."kb_collections" from "anon";

revoke delete on table "public"."kb_collections" from "authenticated";

revoke insert on table "public"."kb_collections" from "authenticated";

revoke references on table "public"."kb_collections" from "authenticated";

revoke select on table "public"."kb_collections" from "authenticated";

revoke trigger on table "public"."kb_collections" from "authenticated";

revoke truncate on table "public"."kb_collections" from "authenticated";

revoke update on table "public"."kb_collections" from "authenticated";

revoke delete on table "public"."kb_documents" from "anon";

revoke insert on table "public"."kb_documents" from "anon";

revoke references on table "public"."kb_documents" from "anon";

revoke select on table "public"."kb_documents" from "anon";

revoke trigger on table "public"."kb_documents" from "anon";

revoke truncate on table "public"."kb_documents" from "anon";

revoke update on table "public"."kb_documents" from "anon";

revoke delete on table "public"."kb_documents" from "authenticated";

revoke insert on table "public"."kb_documents" from "authenticated";

revoke references on table "public"."kb_documents" from "authenticated";

revoke select on table "public"."kb_documents" from "authenticated";

revoke trigger on table "public"."kb_documents" from "authenticated";

revoke truncate on table "public"."kb_documents" from "authenticated";

revoke update on table "public"."kb_documents" from "authenticated";

revoke delete on table "public"."laban_orders" from "anon";

revoke insert on table "public"."laban_orders" from "anon";

revoke references on table "public"."laban_orders" from "anon";

revoke select on table "public"."laban_orders" from "anon";

revoke trigger on table "public"."laban_orders" from "anon";

revoke truncate on table "public"."laban_orders" from "anon";

revoke update on table "public"."laban_orders" from "anon";

revoke delete on table "public"."laban_orders" from "authenticated";

revoke insert on table "public"."laban_orders" from "authenticated";

revoke references on table "public"."laban_orders" from "authenticated";

revoke select on table "public"."laban_orders" from "authenticated";

revoke trigger on table "public"."laban_orders" from "authenticated";

revoke truncate on table "public"."laban_orders" from "authenticated";

revoke update on table "public"."laban_orders" from "authenticated";

revoke delete on table "public"."leads" from "anon";

revoke insert on table "public"."leads" from "anon";

revoke references on table "public"."leads" from "anon";

revoke select on table "public"."leads" from "anon";

revoke trigger on table "public"."leads" from "anon";

revoke truncate on table "public"."leads" from "anon";

revoke update on table "public"."leads" from "anon";

revoke delete on table "public"."leads" from "authenticated";

revoke insert on table "public"."leads" from "authenticated";

revoke references on table "public"."leads" from "authenticated";

revoke select on table "public"."leads" from "authenticated";

revoke trigger on table "public"."leads" from "authenticated";

revoke truncate on table "public"."leads" from "authenticated";

revoke update on table "public"."leads" from "authenticated";

revoke delete on table "public"."maintenance_requests" from "anon";

revoke insert on table "public"."maintenance_requests" from "anon";

revoke references on table "public"."maintenance_requests" from "anon";

revoke select on table "public"."maintenance_requests" from "anon";

revoke trigger on table "public"."maintenance_requests" from "anon";

revoke truncate on table "public"."maintenance_requests" from "anon";

revoke update on table "public"."maintenance_requests" from "anon";

revoke delete on table "public"."maintenance_requests" from "authenticated";

revoke insert on table "public"."maintenance_requests" from "authenticated";

revoke references on table "public"."maintenance_requests" from "authenticated";

revoke select on table "public"."maintenance_requests" from "authenticated";

revoke trigger on table "public"."maintenance_requests" from "authenticated";

revoke truncate on table "public"."maintenance_requests" from "authenticated";

revoke update on table "public"."maintenance_requests" from "authenticated";

revoke delete on table "public"."notifications" from "anon";

revoke insert on table "public"."notifications" from "anon";

revoke references on table "public"."notifications" from "anon";

revoke select on table "public"."notifications" from "anon";

revoke trigger on table "public"."notifications" from "anon";

revoke truncate on table "public"."notifications" from "anon";

revoke update on table "public"."notifications" from "anon";

revoke delete on table "public"."notifications" from "authenticated";

revoke insert on table "public"."notifications" from "authenticated";

revoke references on table "public"."notifications" from "authenticated";

revoke select on table "public"."notifications" from "authenticated";

revoke trigger on table "public"."notifications" from "authenticated";

revoke truncate on table "public"."notifications" from "authenticated";

revoke update on table "public"."notifications" from "authenticated";

revoke delete on table "public"."profiles" from "anon";

revoke insert on table "public"."profiles" from "anon";

revoke references on table "public"."profiles" from "anon";

revoke select on table "public"."profiles" from "anon";

revoke trigger on table "public"."profiles" from "anon";

revoke truncate on table "public"."profiles" from "anon";

revoke update on table "public"."profiles" from "anon";

revoke delete on table "public"."profiles" from "authenticated";

revoke insert on table "public"."profiles" from "authenticated";

revoke references on table "public"."profiles" from "authenticated";

revoke select on table "public"."profiles" from "authenticated";

revoke trigger on table "public"."profiles" from "authenticated";

revoke truncate on table "public"."profiles" from "authenticated";

revoke update on table "public"."profiles" from "authenticated";

revoke delete on table "public"."project_files" from "anon";

revoke insert on table "public"."project_files" from "anon";

revoke references on table "public"."project_files" from "anon";

revoke select on table "public"."project_files" from "anon";

revoke trigger on table "public"."project_files" from "anon";

revoke truncate on table "public"."project_files" from "anon";

revoke update on table "public"."project_files" from "anon";

revoke delete on table "public"."project_files" from "authenticated";

revoke insert on table "public"."project_files" from "authenticated";

revoke references on table "public"."project_files" from "authenticated";

revoke select on table "public"."project_files" from "authenticated";

revoke trigger on table "public"."project_files" from "authenticated";

revoke truncate on table "public"."project_files" from "authenticated";

revoke update on table "public"."project_files" from "authenticated";

revoke delete on table "public"."project_members" from "anon";

revoke insert on table "public"."project_members" from "anon";

revoke references on table "public"."project_members" from "anon";

revoke select on table "public"."project_members" from "anon";

revoke trigger on table "public"."project_members" from "anon";

revoke truncate on table "public"."project_members" from "anon";

revoke update on table "public"."project_members" from "anon";

revoke delete on table "public"."project_members" from "authenticated";

revoke insert on table "public"."project_members" from "authenticated";

revoke references on table "public"."project_members" from "authenticated";

revoke select on table "public"."project_members" from "authenticated";

revoke trigger on table "public"."project_members" from "authenticated";

revoke truncate on table "public"."project_members" from "authenticated";

revoke update on table "public"."project_members" from "authenticated";

revoke delete on table "public"."projects" from "anon";

revoke insert on table "public"."projects" from "anon";

revoke references on table "public"."projects" from "anon";

revoke select on table "public"."projects" from "anon";

revoke trigger on table "public"."projects" from "anon";

revoke truncate on table "public"."projects" from "anon";

revoke update on table "public"."projects" from "anon";

revoke delete on table "public"."projects" from "authenticated";

revoke insert on table "public"."projects" from "authenticated";

revoke references on table "public"."projects" from "authenticated";

revoke select on table "public"."projects" from "authenticated";

revoke trigger on table "public"."projects" from "authenticated";

revoke truncate on table "public"."projects" from "authenticated";

revoke update on table "public"."projects" from "authenticated";

revoke delete on table "public"."user_roles" from "anon";

revoke insert on table "public"."user_roles" from "anon";

revoke references on table "public"."user_roles" from "anon";

revoke select on table "public"."user_roles" from "anon";

revoke trigger on table "public"."user_roles" from "anon";

revoke truncate on table "public"."user_roles" from "anon";

revoke update on table "public"."user_roles" from "anon";

revoke delete on table "public"."user_roles" from "authenticated";

revoke insert on table "public"."user_roles" from "authenticated";

revoke references on table "public"."user_roles" from "authenticated";

revoke select on table "public"."user_roles" from "authenticated";

revoke trigger on table "public"."user_roles" from "authenticated";

revoke truncate on table "public"."user_roles" from "authenticated";

revoke update on table "public"."user_roles" from "authenticated";

revoke delete on table "public"."whatsapp_integrations" from "anon";

revoke insert on table "public"."whatsapp_integrations" from "anon";

revoke references on table "public"."whatsapp_integrations" from "anon";

revoke select on table "public"."whatsapp_integrations" from "anon";

revoke trigger on table "public"."whatsapp_integrations" from "anon";

revoke truncate on table "public"."whatsapp_integrations" from "anon";

revoke update on table "public"."whatsapp_integrations" from "anon";

revoke delete on table "public"."whatsapp_integrations" from "authenticated";

revoke insert on table "public"."whatsapp_integrations" from "authenticated";

revoke references on table "public"."whatsapp_integrations" from "authenticated";

revoke select on table "public"."whatsapp_integrations" from "authenticated";

revoke trigger on table "public"."whatsapp_integrations" from "authenticated";

revoke truncate on table "public"."whatsapp_integrations" from "authenticated";

revoke update on table "public"."whatsapp_integrations" from "authenticated";

revoke delete on table "public"."whatsapp_media" from "anon";

revoke insert on table "public"."whatsapp_media" from "anon";

revoke references on table "public"."whatsapp_media" from "anon";

revoke select on table "public"."whatsapp_media" from "anon";

revoke trigger on table "public"."whatsapp_media" from "anon";

revoke truncate on table "public"."whatsapp_media" from "anon";

revoke update on table "public"."whatsapp_media" from "anon";

revoke delete on table "public"."whatsapp_media" from "authenticated";

revoke insert on table "public"."whatsapp_media" from "authenticated";

revoke references on table "public"."whatsapp_media" from "authenticated";

revoke select on table "public"."whatsapp_media" from "authenticated";

revoke trigger on table "public"."whatsapp_media" from "authenticated";

revoke truncate on table "public"."whatsapp_media" from "authenticated";

revoke update on table "public"."whatsapp_media" from "authenticated";

revoke delete on table "public"."whatsapp_message_templates" from "anon";

revoke insert on table "public"."whatsapp_message_templates" from "anon";

revoke references on table "public"."whatsapp_message_templates" from "anon";

revoke select on table "public"."whatsapp_message_templates" from "anon";

revoke trigger on table "public"."whatsapp_message_templates" from "anon";

revoke truncate on table "public"."whatsapp_message_templates" from "anon";

revoke update on table "public"."whatsapp_message_templates" from "anon";

revoke delete on table "public"."whatsapp_message_templates" from "authenticated";

revoke insert on table "public"."whatsapp_message_templates" from "authenticated";

revoke references on table "public"."whatsapp_message_templates" from "authenticated";

revoke select on table "public"."whatsapp_message_templates" from "authenticated";

revoke trigger on table "public"."whatsapp_message_templates" from "authenticated";

revoke truncate on table "public"."whatsapp_message_templates" from "authenticated";

revoke update on table "public"."whatsapp_message_templates" from "authenticated";

revoke delete on table "public"."whatsapp_messages" from "anon";

revoke insert on table "public"."whatsapp_messages" from "anon";

revoke references on table "public"."whatsapp_messages" from "anon";

revoke select on table "public"."whatsapp_messages" from "anon";

revoke trigger on table "public"."whatsapp_messages" from "anon";

revoke truncate on table "public"."whatsapp_messages" from "anon";

revoke update on table "public"."whatsapp_messages" from "anon";

revoke delete on table "public"."whatsapp_messages" from "authenticated";

revoke insert on table "public"."whatsapp_messages" from "authenticated";

revoke references on table "public"."whatsapp_messages" from "authenticated";

revoke select on table "public"."whatsapp_messages" from "authenticated";

revoke trigger on table "public"."whatsapp_messages" from "authenticated";

revoke truncate on table "public"."whatsapp_messages" from "authenticated";

revoke update on table "public"."whatsapp_messages" from "authenticated";

revoke delete on table "public"."whatsapp_templates" from "anon";

revoke insert on table "public"."whatsapp_templates" from "anon";

revoke references on table "public"."whatsapp_templates" from "anon";

revoke select on table "public"."whatsapp_templates" from "anon";

revoke trigger on table "public"."whatsapp_templates" from "anon";

revoke truncate on table "public"."whatsapp_templates" from "anon";

revoke update on table "public"."whatsapp_templates" from "anon";

revoke delete on table "public"."whatsapp_templates" from "authenticated";

revoke insert on table "public"."whatsapp_templates" from "authenticated";

revoke references on table "public"."whatsapp_templates" from "authenticated";

revoke select on table "public"."whatsapp_templates" from "authenticated";

revoke trigger on table "public"."whatsapp_templates" from "authenticated";

revoke truncate on table "public"."whatsapp_templates" from "authenticated";

revoke update on table "public"."whatsapp_templates" from "authenticated";

alter table "public"."whatsapp_templates" drop constraint "whatsapp_templates_integration_id_fkey";


  create table "public"."api_consumers" (
    "id" uuid not null default gen_random_uuid(),
    "name" text not null,
    "channel" text not null default 'api'::text,
    "api_key" text,
    "api_key_hash" text,
    "api_key_last4" text,
    "is_active" boolean not null default true,
    "rate_limit_per_minute" integer not null default 60,
    "allowed_origins" text[] not null default ARRAY[]::text[],
    "company_id" uuid,
    "branch_id" uuid,
    "created_at" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone not null default now()
      );


alter table "public"."api_consumers" enable row level security;


  create table "public"."api_gateway_logs" (
    "id" uuid not null default gen_random_uuid(),
    "consumer_id" uuid,
    "route" text not null,
    "action" text,
    "request_payload" jsonb,
    "response_payload" jsonb,
    "status_code" integer,
    "success" boolean,
    "duration_ms" integer,
    "ip_address" inet,
    "user_agent" text,
    "error_message" text,
    "created_at" timestamp with time zone not null default now()
      );


alter table "public"."api_gateway_logs" enable row level security;


  create table "public"."audit_logs" (
    "id" uuid not null default gen_random_uuid(),
    "actor_type" text not null default 'bot'::text,
    "actor_id" text,
    "action" text not null,
    "entity_type" text,
    "entity_id" uuid,
    "old_values" jsonb,
    "new_values" jsonb,
    "metadata" jsonb not null default '{}'::jsonb,
    "created_at" timestamp with time zone not null default now()
      );


alter table "public"."audit_logs" enable row level security;


  create table "public"."bot_sessions" (
    "id" uuid not null default gen_random_uuid(),
    "session_id" text not null,
    "client_phone" text,
    "client_name" text,
    "client_email" text,
    "location" text,
    "latitude" numeric(10,7),
    "longitude" numeric(10,7),
    "preferred_branch_id" uuid,
    "context" jsonb not null default '{}'::jsonb,
    "expires_at" timestamp with time zone not null default (now() + '7 days'::interval),
    "created_at" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone not null default now()
      );


alter table "public"."bot_sessions" enable row level security;


  create table "public"."branches" (
    "id" uuid not null default gen_random_uuid(),
    "name" text not null,
    "city" text,
    "address" text,
    "latitude" numeric(10,7),
    "longitude" numeric(10,7),
    "phone" text,
    "is_active" boolean not null default true,
    "created_at" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone not null default now()
      );


alter table "public"."branches" enable row level security;


  create table "public"."brands" (
    "id" uuid not null default gen_random_uuid(),
    "key" text not null,
    "name" text not null,
    "bot_persona" text not null default 'المساعد الذكي'::text,
    "system_prompt" text not null,
    "allowed_origins" text[] not null default ARRAY[]::text[],
    "domains" text[] not null default ARRAY[]::text[],
    "ai_engine" text not null default 'gemini'::text,
    "created_at" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone not null default now()
      );


alter table "public"."brands" enable row level security;


  create table "public"."escalation_tickets" (
    "id" uuid not null default gen_random_uuid(),
    "sender_id" text,
    "reason" text,
    "description" text,
    "brand" text,
    "status" text default 'open'::text,
    "created_at" timestamp with time zone not null default now()
      );


alter table "public"."escalation_tickets" enable row level security;


  create table "public"."events" (
    "id" integer not null default nextval('public.events_id_seq'::regclass),
    "sender_id" character varying(255) not null,
    "type_name" character varying(255) not null,
    "timestamp" double precision,
    "intent_name" character varying(255),
    "action_name" character varying(255),
    "data" text
      );


alter table "public"."events" enable row level security;


  create table "public"."feedback" (
    "id" uuid not null default gen_random_uuid(),
    "sender_id" text,
    "service" text,
    "rating" numeric(2,1),
    "feedback_text" text,
    "brand" text,
    "created_at" timestamp with time zone not null default now()
      );


alter table "public"."feedback" enable row level security;


  create table "public"."maintenance_categories" (
    "id" uuid not null default gen_random_uuid(),
    "key" text not null,
    "label_ar" text not null,
    "label_en" text,
    "is_active" boolean not null default true,
    "sort_order" integer not null default 100,
    "created_at" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone not null default now()
      );


alter table "public"."maintenance_categories" enable row level security;


  create table "public"."maintenance_request_notes" (
    "id" uuid not null default gen_random_uuid(),
    "request_id" uuid not null,
    "note" text not null,
    "note_type" text not null default 'customer'::text,
    "created_by" text,
    "created_at" timestamp with time zone not null default now()
      );


alter table "public"."maintenance_request_notes" enable row level security;


  create table "public"."maintenance_technicians" (
    "id" uuid not null default gen_random_uuid(),
    "name" text not null,
    "phone" text,
    "specialization" text,
    "city_id" uuid,
    "rating" numeric(3,2) default 0,
    "review_count" integer not null default 0,
    "tier" text,
    "latitude" numeric(10,7),
    "longitude" numeric(10,7),
    "is_active" boolean not null default true,
    "is_verified" boolean not null default false,
    "created_at" timestamp with time zone not null default now(),
    "updated_at" timestamp with time zone not null default now()
      );


alter table "public"."maintenance_technicians" enable row level security;


  create table "public"."outbound_messages" (
    "id" uuid not null default gen_random_uuid(),
    "request_id" uuid,
    "channel" text not null default 'whatsapp'::text,
    "recipient" text not null,
    "message" text not null,
    "payload" jsonb not null default '{}'::jsonb,
    "status" text not null default 'pending'::text,
    "provider_response" jsonb,
    "error_message" text,
    "scheduled_at" timestamp with time zone not null default now(),
    "sent_at" timestamp with time zone,
    "created_at" timestamp with time zone not null default now()
      );


alter table "public"."outbound_messages" enable row level security;


  create table "public"."suggestions" (
    "id" uuid not null default gen_random_uuid(),
    "sender_id" text,
    "suggestion" text,
    "brand" text,
    "created_at" timestamp with time zone not null default now()
      );


alter table "public"."suggestions" enable row level security;


  create table "public"."users" (
    "sender_id" character varying(255) not null,
    "user_id" character varying(255) not null,
    "conversation_started_timestamp" double precision
      );


alter table "public"."users" enable row level security;

alter table "public"."conversations" add column "updated_at" timestamp with time zone not null default now();

alter table "public"."leads" drop column "channel";

alter table "public"."leads" drop column "user_message";

alter table "public"."leads" drop column "user_name";

alter table "public"."leads" drop column "user_phone";

alter table "public"."leads" add column "name" text;

alter table "public"."leads" add column "phone" text;

alter table "public"."leads" add column "sender_id" text;

alter table "public"."leads" alter column "metadata" set not null;

alter table "public"."leads" alter column "source" set default 'chatbot'::text;

alter table "public"."maintenance_requests" add column "client_phone" text;

alter table "public"."maintenance_requests" add column "daftra_client_id" text;

alter table "public"."maintenance_requests" add column "daftra_document_url" text;

alter table "public"."maintenance_requests" add column "daftra_invoice_id" text;

alter table "public"."maintenance_requests" add column "daftra_invoice_number" text;

alter table "public"."maintenance_requests" add column "payment_status" text default 'unpaid'::text;

alter table "public"."maintenance_requests" add column "request_number" text default public.next_maintenance_request_number();

alter table "public"."maintenance_requests" add column "workflow_stage" text default 'submitted'::text;

alter table "public"."whatsapp_templates" drop column "body";

alter table "public"."whatsapp_templates" drop column "integration_id";

alter table "public"."whatsapp_templates" drop column "name";

alter table "public"."whatsapp_templates" drop column "status";

alter table "public"."whatsapp_templates" drop column "template_id";

alter table "public"."whatsapp_templates" drop column "variables";

alter table "public"."whatsapp_templates" add column "body_text" text not null;

alter table "public"."whatsapp_templates" add column "category" character varying(100);

alter table "public"."whatsapp_templates" add column "language_code" character varying(10) default 'ar'::character varying;

alter table "public"."whatsapp_templates" add column "template_name" character varying(255) not null;

alter table "public"."whatsapp_templates" add column "updated_at" timestamp without time zone default CURRENT_TIMESTAMP;

alter table "public"."whatsapp_templates" alter column "created_at" set default CURRENT_TIMESTAMP;

alter table "public"."whatsapp_templates" alter column "id" set default nextval('public.whatsapp_templates_id_seq'::regclass);

alter table "public"."whatsapp_templates" alter column "id" set data type integer using "id"::integer;

alter sequence "public"."events_id_seq" owned by "public"."events"."id";

alter sequence "public"."whatsapp_templates_id_seq" owned by "public"."whatsapp_templates"."id";

CREATE UNIQUE INDEX api_consumers_api_key_key ON public.api_consumers USING btree (api_key);

CREATE UNIQUE INDEX api_consumers_name_key ON public.api_consumers USING btree (name);

CREATE UNIQUE INDEX api_consumers_pkey ON public.api_consumers USING btree (id);

CREATE UNIQUE INDEX api_gateway_logs_pkey ON public.api_gateway_logs USING btree (id);

CREATE UNIQUE INDEX audit_logs_pkey ON public.audit_logs USING btree (id);

CREATE UNIQUE INDEX bot_sessions_pkey ON public.bot_sessions USING btree (id);

CREATE UNIQUE INDEX bot_sessions_session_id_key ON public.bot_sessions USING btree (session_id);

CREATE UNIQUE INDEX branches_pkey ON public.branches USING btree (id);

CREATE UNIQUE INDEX brands_key_key ON public.brands USING btree (key);

CREATE UNIQUE INDEX brands_pkey ON public.brands USING btree (id);

CREATE UNIQUE INDEX escalation_tickets_pkey ON public.escalation_tickets USING btree (id);

CREATE UNIQUE INDEX events_pkey ON public.events USING btree (id);

CREATE UNIQUE INDEX feedback_pkey ON public.feedback USING btree (id);

CREATE INDEX idx_api_gateway_logs_action_created ON public.api_gateway_logs USING btree (action, created_at DESC);

CREATE INDEX idx_api_gateway_logs_consumer_created ON public.api_gateway_logs USING btree (consumer_id, created_at DESC);

CREATE INDEX idx_audit_logs_entity ON public.audit_logs USING btree (entity_type, entity_id, created_at DESC);

CREATE INDEX idx_bot_sessions_expires ON public.bot_sessions USING btree (expires_at);

CREATE INDEX idx_bot_sessions_phone ON public.bot_sessions USING btree (client_phone);

CREATE INDEX idx_maintenance_requests_created ON public.maintenance_requests USING btree (created_at DESC);

CREATE INDEX idx_maintenance_requests_phone ON public.maintenance_requests USING btree (client_phone);

CREATE INDEX idx_maintenance_requests_status ON public.maintenance_requests USING btree (status, workflow_stage);

CREATE INDEX idx_outbound_messages_status ON public.outbound_messages USING btree (status, scheduled_at);

CREATE INDEX idx_technicians_specialization ON public.maintenance_technicians USING btree (specialization, is_active, is_verified);

CREATE INDEX ix_events_sender_id ON public.events USING btree (sender_id);

CREATE INDEX ix_users_conversation_started_timestamp ON public.users USING btree (conversation_started_timestamp);

CREATE INDEX ix_users_sender_id ON public.users USING btree (sender_id);

CREATE INDEX ix_users_user_id ON public.users USING btree (user_id);

CREATE UNIQUE INDEX maintenance_categories_key_key ON public.maintenance_categories USING btree (key);

CREATE UNIQUE INDEX maintenance_categories_pkey ON public.maintenance_categories USING btree (id);

CREATE UNIQUE INDEX maintenance_request_notes_pkey ON public.maintenance_request_notes USING btree (id);

CREATE UNIQUE INDEX maintenance_technicians_pkey ON public.maintenance_technicians USING btree (id);

CREATE UNIQUE INDEX outbound_messages_pkey ON public.outbound_messages USING btree (id);

CREATE UNIQUE INDEX suggestions_pkey ON public.suggestions USING btree (id);

CREATE UNIQUE INDEX users_pkey ON public.users USING btree (sender_id);

CREATE UNIQUE INDEX whatsapp_templates_template_name_key ON public.whatsapp_templates USING btree (template_name);

alter table "public"."api_consumers" add constraint "api_consumers_pkey" PRIMARY KEY using index "api_consumers_pkey";

alter table "public"."api_gateway_logs" add constraint "api_gateway_logs_pkey" PRIMARY KEY using index "api_gateway_logs_pkey";

alter table "public"."audit_logs" add constraint "audit_logs_pkey" PRIMARY KEY using index "audit_logs_pkey";

alter table "public"."bot_sessions" add constraint "bot_sessions_pkey" PRIMARY KEY using index "bot_sessions_pkey";

alter table "public"."branches" add constraint "branches_pkey" PRIMARY KEY using index "branches_pkey";

alter table "public"."brands" add constraint "brands_pkey" PRIMARY KEY using index "brands_pkey";

alter table "public"."escalation_tickets" add constraint "escalation_tickets_pkey" PRIMARY KEY using index "escalation_tickets_pkey";

alter table "public"."events" add constraint "events_pkey" PRIMARY KEY using index "events_pkey";

alter table "public"."feedback" add constraint "feedback_pkey" PRIMARY KEY using index "feedback_pkey";

alter table "public"."maintenance_categories" add constraint "maintenance_categories_pkey" PRIMARY KEY using index "maintenance_categories_pkey";

alter table "public"."maintenance_request_notes" add constraint "maintenance_request_notes_pkey" PRIMARY KEY using index "maintenance_request_notes_pkey";

alter table "public"."maintenance_technicians" add constraint "maintenance_technicians_pkey" PRIMARY KEY using index "maintenance_technicians_pkey";

alter table "public"."outbound_messages" add constraint "outbound_messages_pkey" PRIMARY KEY using index "outbound_messages_pkey";

alter table "public"."suggestions" add constraint "suggestions_pkey" PRIMARY KEY using index "suggestions_pkey";

alter table "public"."users" add constraint "users_pkey" PRIMARY KEY using index "users_pkey";

alter table "public"."api_consumers" add constraint "api_consumers_api_key_key" UNIQUE using index "api_consumers_api_key_key";

alter table "public"."api_consumers" add constraint "api_consumers_name_key" UNIQUE using index "api_consumers_name_key";

alter table "public"."api_consumers" add constraint "api_consumers_rate_limit_per_minute_check" CHECK ((rate_limit_per_minute > 0)) not valid;

alter table "public"."api_consumers" validate constraint "api_consumers_rate_limit_per_minute_check";

alter table "public"."api_gateway_logs" add constraint "api_gateway_logs_consumer_id_fkey" FOREIGN KEY (consumer_id) REFERENCES public.api_consumers(id) ON DELETE SET NULL not valid;

alter table "public"."api_gateway_logs" validate constraint "api_gateway_logs_consumer_id_fkey";

alter table "public"."bot_sessions" add constraint "bot_sessions_session_id_key" UNIQUE using index "bot_sessions_session_id_key";

alter table "public"."brands" add constraint "brands_ai_engine_check" CHECK ((ai_engine = ANY (ARRAY['gemini'::text, 'dialogflow'::text]))) not valid;

alter table "public"."brands" validate constraint "brands_ai_engine_check";

alter table "public"."brands" add constraint "brands_key_key" UNIQUE using index "brands_key_key";

alter table "public"."maintenance_categories" add constraint "maintenance_categories_key_key" UNIQUE using index "maintenance_categories_key_key";

alter table "public"."maintenance_request_notes" add constraint "maintenance_request_notes_request_id_fkey" FOREIGN KEY (request_id) REFERENCES public.maintenance_requests(id) ON DELETE CASCADE not valid;

alter table "public"."maintenance_request_notes" validate constraint "maintenance_request_notes_request_id_fkey";

alter table "public"."outbound_messages" add constraint "outbound_messages_request_id_fkey" FOREIGN KEY (request_id) REFERENCES public.maintenance_requests(id) ON DELETE SET NULL not valid;

alter table "public"."outbound_messages" validate constraint "outbound_messages_request_id_fkey";

alter table "public"."whatsapp_templates" add constraint "whatsapp_templates_template_name_key" UNIQUE using index "whatsapp_templates_template_name_key";

set check_function_bodies = off;

CREATE OR REPLACE FUNCTION public.next_maintenance_request_number()
 RETURNS text
 LANGUAGE plpgsql
 SET search_path TO 'public'
AS $function$
DECLARE
    next_num bigint;
    yy text;
BEGIN
    next_num := nextval('maintenance_request_number_seq');
    yy := to_char(now(), 'YY');
    RETURN 'MR-' || yy || '-' || lpad(next_num::text, 5, '0');
END;
$function$
;

CREATE OR REPLACE FUNCTION public.set_updated_at()
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

grant delete on table "public"."api_consumers" to "service_role";

grant insert on table "public"."api_consumers" to "service_role";

grant references on table "public"."api_consumers" to "service_role";

grant select on table "public"."api_consumers" to "service_role";

grant trigger on table "public"."api_consumers" to "service_role";

grant truncate on table "public"."api_consumers" to "service_role";

grant update on table "public"."api_consumers" to "service_role";

grant delete on table "public"."api_gateway_logs" to "service_role";

grant insert on table "public"."api_gateway_logs" to "service_role";

grant references on table "public"."api_gateway_logs" to "service_role";

grant select on table "public"."api_gateway_logs" to "service_role";

grant trigger on table "public"."api_gateway_logs" to "service_role";

grant truncate on table "public"."api_gateway_logs" to "service_role";

grant update on table "public"."api_gateway_logs" to "service_role";

grant delete on table "public"."audit_logs" to "service_role";

grant insert on table "public"."audit_logs" to "service_role";

grant references on table "public"."audit_logs" to "service_role";

grant select on table "public"."audit_logs" to "service_role";

grant trigger on table "public"."audit_logs" to "service_role";

grant truncate on table "public"."audit_logs" to "service_role";

grant update on table "public"."audit_logs" to "service_role";

grant delete on table "public"."bot_sessions" to "service_role";

grant insert on table "public"."bot_sessions" to "service_role";

grant references on table "public"."bot_sessions" to "service_role";

grant select on table "public"."bot_sessions" to "service_role";

grant trigger on table "public"."bot_sessions" to "service_role";

grant truncate on table "public"."bot_sessions" to "service_role";

grant update on table "public"."bot_sessions" to "service_role";

grant delete on table "public"."branches" to "service_role";

grant insert on table "public"."branches" to "service_role";

grant references on table "public"."branches" to "service_role";

grant select on table "public"."branches" to "service_role";

grant trigger on table "public"."branches" to "service_role";

grant truncate on table "public"."branches" to "service_role";

grant update on table "public"."branches" to "service_role";

grant delete on table "public"."brands" to "service_role";

grant insert on table "public"."brands" to "service_role";

grant references on table "public"."brands" to "service_role";

grant select on table "public"."brands" to "service_role";

grant trigger on table "public"."brands" to "service_role";

grant truncate on table "public"."brands" to "service_role";

grant update on table "public"."brands" to "service_role";

grant delete on table "public"."escalation_tickets" to "service_role";

grant insert on table "public"."escalation_tickets" to "service_role";

grant references on table "public"."escalation_tickets" to "service_role";

grant select on table "public"."escalation_tickets" to "service_role";

grant trigger on table "public"."escalation_tickets" to "service_role";

grant truncate on table "public"."escalation_tickets" to "service_role";

grant update on table "public"."escalation_tickets" to "service_role";

grant delete on table "public"."events" to "service_role";

grant insert on table "public"."events" to "service_role";

grant references on table "public"."events" to "service_role";

grant select on table "public"."events" to "service_role";

grant trigger on table "public"."events" to "service_role";

grant truncate on table "public"."events" to "service_role";

grant update on table "public"."events" to "service_role";

grant delete on table "public"."feedback" to "service_role";

grant insert on table "public"."feedback" to "service_role";

grant references on table "public"."feedback" to "service_role";

grant select on table "public"."feedback" to "service_role";

grant trigger on table "public"."feedback" to "service_role";

grant truncate on table "public"."feedback" to "service_role";

grant update on table "public"."feedback" to "service_role";

grant delete on table "public"."maintenance_categories" to "service_role";

grant insert on table "public"."maintenance_categories" to "service_role";

grant references on table "public"."maintenance_categories" to "service_role";

grant select on table "public"."maintenance_categories" to "service_role";

grant trigger on table "public"."maintenance_categories" to "service_role";

grant truncate on table "public"."maintenance_categories" to "service_role";

grant update on table "public"."maintenance_categories" to "service_role";

grant delete on table "public"."maintenance_request_notes" to "service_role";

grant insert on table "public"."maintenance_request_notes" to "service_role";

grant references on table "public"."maintenance_request_notes" to "service_role";

grant select on table "public"."maintenance_request_notes" to "service_role";

grant trigger on table "public"."maintenance_request_notes" to "service_role";

grant truncate on table "public"."maintenance_request_notes" to "service_role";

grant update on table "public"."maintenance_request_notes" to "service_role";

grant delete on table "public"."maintenance_technicians" to "service_role";

grant insert on table "public"."maintenance_technicians" to "service_role";

grant references on table "public"."maintenance_technicians" to "service_role";

grant select on table "public"."maintenance_technicians" to "service_role";

grant trigger on table "public"."maintenance_technicians" to "service_role";

grant truncate on table "public"."maintenance_technicians" to "service_role";

grant update on table "public"."maintenance_technicians" to "service_role";

grant delete on table "public"."outbound_messages" to "service_role";

grant insert on table "public"."outbound_messages" to "service_role";

grant references on table "public"."outbound_messages" to "service_role";

grant select on table "public"."outbound_messages" to "service_role";

grant trigger on table "public"."outbound_messages" to "service_role";

grant truncate on table "public"."outbound_messages" to "service_role";

grant update on table "public"."outbound_messages" to "service_role";

grant delete on table "public"."suggestions" to "service_role";

grant insert on table "public"."suggestions" to "service_role";

grant references on table "public"."suggestions" to "service_role";

grant select on table "public"."suggestions" to "service_role";

grant trigger on table "public"."suggestions" to "service_role";

grant truncate on table "public"."suggestions" to "service_role";

grant update on table "public"."suggestions" to "service_role";

grant delete on table "public"."users" to "service_role";

grant insert on table "public"."users" to "service_role";

grant references on table "public"."users" to "service_role";

grant select on table "public"."users" to "service_role";

grant trigger on table "public"."users" to "service_role";

grant truncate on table "public"."users" to "service_role";

grant update on table "public"."users" to "service_role";


  create policy "Service Role Full Access"
  on "public"."admin_auth"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."api_consumers"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."api_gateway_logs"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."audit_logs"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."bot_sessions"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."bot_settings"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "anon_read_settings"
  on "public"."bot_settings"
  as permissive
  for select
  to anon
using (true);



  create policy "service_role_settings"
  on "public"."bot_settings"
  as permissive
  for all
  to service_role
using (true);



  create policy "Service Role Full Access"
  on "public"."branches"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."brands"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "anon_read_brands"
  on "public"."brands"
  as permissive
  for select
  to anon
using (true);



  create policy "service_role_brands"
  on "public"."brands"
  as permissive
  for all
  to service_role
using (true);



  create policy "Service Role Full Access"
  on "public"."cloud_storage_providers"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."conversations"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."daftra_transactions"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."escalation_tickets"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."events"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."feedback"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."file_comments"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."integrations"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."kb_collections"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."kb_documents"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."laban_orders"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."leads"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."maintenance_categories"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."maintenance_request_notes"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."maintenance_requests"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."maintenance_technicians"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."messages"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."notifications"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."outbound_messages"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."profiles"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."project_files"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."project_members"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."projects"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."suggestions"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."user_roles"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."users"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."webhook_logs"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."whatsapp_integrations"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."whatsapp_media"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."whatsapp_message_templates"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."whatsapp_messages"
  as permissive
  for all
  to service_role
using (true)
with check (true);



  create policy "Service Role Full Access"
  on "public"."whatsapp_templates"
  as permissive
  for all
  to service_role
using (true)
with check (true);


CREATE TRIGGER trg_api_consumers_updated_at BEFORE UPDATE ON public.api_consumers FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_bot_sessions_updated_at BEFORE UPDATE ON public.bot_sessions FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_bot_settings_updated_at BEFORE UPDATE ON public.bot_settings FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_branches_updated_at BEFORE UPDATE ON public.branches FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_brands_updated_at BEFORE UPDATE ON public.brands FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_maintenance_categories_updated_at BEFORE UPDATE ON public.maintenance_categories FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_maintenance_requests_updated_at BEFORE UPDATE ON public.maintenance_requests FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_maintenance_technicians_updated_at BEFORE UPDATE ON public.maintenance_technicians FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


  create policy "service_role_audio"
  on "storage"."objects"
  as permissive
  for all
  to service_role
using (true);



  create policy "service_role_uploads"
  on "storage"."objects"
  as permissive
  for all
  to service_role
using (true);



