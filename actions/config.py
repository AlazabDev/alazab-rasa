import os

# Central Configuration for AzaBot Actions
# ========================================

# Supabase / Gateway Settings
GATEWAY_URL = os.getenv("MAINTENANCE_GATEWAY_URL", "https://zrrffsjbfkphridqyais.supabase.co/functions/v1/maintenance-gateway")
API_KEY = os.getenv("AZAB_API_KEY", "0639988287e667c4c7801e34065105f3b80303c6d8d3c2f6dfee45cc7314aebe")

# Knowledge Base Paths
PROD_DATA_PATH = "knowledge/production/"
CATEGORIES_PATH = os.path.join(PROD_DATA_PATH, "categories")

# Notification Settings
NOTIFY_PHONE = os.getenv("NOTIFY_PHONE", "")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL", "")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")

# Daftra Accounting Settings
DAFTRA_SUBDOMAIN = os.getenv("DAFTRA_SUBDOMAIN", "alazab")
DAFTRA_API_KEY = os.getenv("DAFTRA_API_KEY", "77d6931873084f788cb9920639022fce")
DAFTRA_BASE_URL = f"https://{DAFTRA_SUBDOMAIN}.daftra.com/api2"

# Central Database Configuration (PostgreSQL)
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "127.0.0.1"),
    "port":     int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "alazab_core"),
    "user":     os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres")
}
