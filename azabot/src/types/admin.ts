// types/admin.ts - الإصدار النهائي المتكامل

// ============ الأنواع الأساسية الموجودة (محفوظة) ============

export interface AdminStats {
  conversations: number;
  messages: number;
  uploads?: number;
  today: number;
  message_counts?: Record<string, number>;
  total?: number;
  uptime_seconds?: number;
  timestamp?: string;
}

export interface AdminSettings {
  bot_name: string;
  primary_color: string;
  position: "right" | "left";
  welcome_message: string;
  quick_replies: string[];
  ai_model: string;
  system_prompt: string;
  voice_enabled: boolean;
  auto_speak: boolean;
  voice_name: string;
  business_hours_enabled: boolean;
  business_hours?: {
    start?: string;
    end?: string;
  };
  offline_message: string;
}

export interface ConversationSummary {
  id: string;
  session_id: string;
  brand?: string;
  channel?: string;
  message_count: number;
  last_message_at: string;
}

export interface AdminUpload {
  id?: string;
  kind?: "file" | "audio" | string;
  name: string;
  size: number;
  content_type?: string;
  url?: string;
  download_url?: string;
  conversation_id?: string;
  session_id?: string;
  message_id?: string;
  brand?: string;
  channel?: string;
  note?: string;
  created_at?: string;
}

export interface ConversationMessage {
  id: string;
  role: "user" | "assistant" | string;
  content: string;
  created_at: string;
  attachments?: AdminUpload[];
}

export interface ConversationDetail extends ConversationSummary {
  created_at?: string;
  messages: ConversationMessage[];
}

// ============ أنواع التكاملات الموسعة ============

export type IntegrationType = "webhook" | "telegram" | "whatsapp" | "twilio" | "slack" | "discord" | "email";

// تكوينات كل نوع تكامل
export interface WebhookIntegrationConfig {
  url: string;
  secret?: string;
  headers?: Record<string, string>;
  method?: 'POST' | 'PUT' | 'PATCH';
  retry_count?: number;
  timeout_seconds?: number;
}

export interface TelegramIntegrationConfig {
  bot_token: string;
  chat_id: string;
  parse_mode?: 'HTML' | 'MarkdownV2';
  disable_notification?: boolean;
}

export interface WhatsAppIntegrationConfig {
  phone_number_id: string;
  access_token: string;
  recipient: string;
  business_account_id?: string;
}

export interface TwilioIntegrationConfig {
  account_sid: string;
  auth_token: string;
  from: string;
  to: string;
  messaging_service_sid?: string;
}

export interface SlackIntegrationConfig {
  webhook_url: string;
  channel?: string;
  username?: string;
  icon_emoji?: string;
}

export interface DiscordIntegrationConfig {
  webhook_url: string;
  username?: string;
  avatar_url?: string;
  thread_id?: string;
}

export interface EmailIntegrationConfig {
  smtp_host: string;
  smtp_port: number;
  smtp_user: string;
  smtp_password: string;
  from_email: string;
  to_emails: string[];
  use_tls?: boolean;
}

// Union type لجميع إعدادات التكاملات
export type IntegrationConfig = Record<string, unknown> & (
  | WebhookIntegrationConfig
  | TelegramIntegrationConfig
  | WhatsAppIntegrationConfig
  | TwilioIntegrationConfig
  | SlackIntegrationConfig
  | DiscordIntegrationConfig
  | EmailIntegrationConfig
);

// واجهة التكامل الرئيسية (متوافقة مع الموجودة مع دعم الأنواع الموسعة)
export interface AdminIntegration {
  id?: string;
  type: IntegrationType | string;
  name: string;
  enabled: boolean;
  config: Record<string, unknown> | IntegrationConfig;  // مرونة أكبر في الإعدادات الديناميكية
  events: string[];
  created_at?: string;
  updated_at?: string;
  last_test_at?: string;
  last_test_status?: 'success' | 'error';
}

// سجل التكامل (متوافق مع الموجود)
export interface IntegrationLog {
  id: string;
  integration_id?: string;
  integration_type?: string;
  event: string;
  request_payload: unknown;
  status: "success" | "failed" | string;
  status_code?: number | null;
  response_body?: string;
  error_message?: string;
  created_at: string;
}

// ============ أنواع التدريب ============

export interface TrainingJob {
  id: string;
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  model_type: 'rasa' | 'custom';
  source: 'upload' | 'api';
  created_at: string;
  completed_at?: string;
  error_message?: string;
  files: string[];
  stats?: {
    epochs: number;
    accuracy?: number;
    loss?: number;
    validation_loss?: number;
  };
}

// ============ أنواع قاعدة المعرفة ============

export interface KnowledgeBaseDocument {
  id: string;
  name: string;
  type: 'pdf' | 'txt' | 'md' | 'docx' | 'url' | 'csv' | 'json';
  url?: string;
  content?: string;
  status: 'pending' | 'processing' | 'ready' | 'failed';
  chunks_count?: number;
  created_at: string;
  updated_at: string;
  metadata: Record<string, unknown>;
}

export interface KnowledgeBaseCollection {
  id: string;
  name: string;
  description: string;
  document_count: number;
  chunk_count: number;
  created_at: string;
}

// ============ دالة معالجة الأخطاء ============

export const errorMessage = (e: unknown, fallback = "حدث خطأ"): string => {
  if (e instanceof Error) return e.message;
  if (typeof e === 'string') return e;
  if (typeof e === 'object' && e !== null && 'message' in e) return String(e.message);
  return fallback;
};

// ============ دوال مساعدة ============

export const formatBytes = (bytes: number): string => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export const getIntegrationTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    webhook: 'Webhook',
    telegram: 'Telegram',
    whatsapp: 'WhatsApp Business',
    twilio: 'Twilio',
    slack: 'Slack',
    discord: 'Discord',
    email: 'البريد الإلكتروني'
  };
  return labels[type] || type;
};