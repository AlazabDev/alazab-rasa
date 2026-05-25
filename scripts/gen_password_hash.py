#!/usr/bin/env python3
"""
scripts/gen_password_hash.py
=============================
أداة توليد bcrypt hash لكلمات مرور الأدمن.

الاستخدام:
  python scripts/gen_password_hash.py

ثم ضع الـ hash الناتج في .env:
  ADMIN_PASSWORD_HASH_ADMIN=$2b$12$...
  ADMIN_PASSWORD_HASH_DEVOPS=$2b$12$...
  ADMIN_PASSWORD_HASH_CEO=$2b$12$...
  ADMIN_PASSWORD_HASH_MOHAMED=$2b$12$...
"""
import getpass
import sys

try:
    import bcrypt
except ImportError:
    print("تثبيت bcrypt أولاً: pip install bcrypt")
    sys.exit(1)

USERS = [
    ("admin@alazab.com",   "ADMIN_PASSWORD_HASH_ADMIN"),
    ("devops@alazab.com",  "ADMIN_PASSWORD_HASH_DEVOPS"),
    ("ceo@alazab.com",     "ADMIN_PASSWORD_HASH_CEO"),
    ("mohamed@alazab.com", "ADMIN_PASSWORD_HASH_MOHAMED"),
]

print("=" * 55)
print("  AzaBot — مولّد bcrypt hash لكلمات المرور")
print("  أضف الناتج لملف .env")
print("=" * 55)
print()

results = []
for email, env_key in USERS:
    print(f"المستخدم: {email}")
    while True:
        pwd  = getpass.getpass("  كلمة المرور: ")
        pwd2 = getpass.getpass("  أعد الكتابة: ")
        if pwd == pwd2:
            break
        print("  ❌ كلمات المرور غير متطابقة — أعد المحاولة")
    if not pwd:
        print(f"  ⚠️  تخطي {email} — كلمة المرور فارغة")
        continue
    hashed = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt(12)).decode()
    results.append((env_key, hashed))
    print(f"  ✅ {env_key}=<hash جاهز>")
    print()

if results:
    print()
    print("=" * 55)
    print("  أضف هذه السطور لـ .env:")
    print("=" * 55)
    for key, val in results:
        print(f"{key}={val}")
    print()
    # توليد ADMIN_SESSION_SECRET
    import secrets
    print(f"ADMIN_SESSION_SECRET={secrets.token_urlsafe(32)}")
    print(f"ADMIN_API_KEY={secrets.token_urlsafe(24)}")
