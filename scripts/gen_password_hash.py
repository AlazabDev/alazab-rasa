#!/usr/bin/env python3
"""scripts/gen_password_hash.py — يولّد bcrypt hash لكلمات مرور الأدمن"""
import getpass, sys
try:
    import bcrypt
except ImportError:
    print("pip install bcrypt"); sys.exit(1)

USERS = [("admin@alazab.com","ADMIN_PASSWORD_HASH_ADMIN"),("devops@alazab.com","ADMIN_PASSWORD_HASH_DEVOPS"),
          ("ceo@alazab.com","ADMIN_PASSWORD_HASH_CEO"),("mohamed@alazab.com","ADMIN_PASSWORD_HASH_MOHAMED")]
print("=" * 50, "\nAzaBot — مولّد bcrypt hash — أضف الناتج لـ .env\n" + "=" * 50)
results = []
for email, key in USERS:
    print(f"\n{email}")
    pwd = getpass.getpass("  كلمة المرور: ")
    if not pwd:
        print("  تخطي"); continue
    h = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt(12)).decode()
    results.append((key, h))
print("\n" + "="*50 + "\nأضف هذه السطور لـ .env:\n" + "="*50)
for k, v in results: print(f"{k}={v}")
import secrets
print(f"ADMIN_SESSION_SECRET={secrets.token_urlsafe(32)}")
