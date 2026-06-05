-- ══════════════════════════════════════════════════════════════
-- db/whatsapp_templates.sql
-- جدول قوالب رسائل الواتساب لمجموعة العزب
-- ══════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS whatsapp_templates (
    id SERIAL PRIMARY KEY,
    template_name VARCHAR(255) NOT NULL UNIQUE,
    language_code VARCHAR(10) DEFAULT 'ar',
    category VARCHAR(100),
    body_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- إدراج بعض القوالب الافتراضية
INSERT INTO whatsapp_templates (template_name, category, body_text) VALUES 
('welcome_message', 'marketing', 'مرحباً بك في مجموعة العزب! كيف يمكننا مساعدتك اليوم؟'),
('maintenance_ticket_created', 'utility', 'تم استلام طلب الصيانة الخاص بك بنجاح. رقم الطلب هو: {{order_number}}'),
('daftra_invoice_sent', 'utility', 'مرحباً، مرفق لك فاتورة الدفع الخاصة بطلبك. شكراً لثقتكم.');
