# ══════════════════════════════════════════════════════════════
# AzaBot v4.0 — Makefile
# الاستخدام: make <command>
# ══════════════════════════════════════════════════════════════

.PHONY: help setup train run-actions run-rasa run-webhook run test clean

help:
	@echo "AzaBot v4.0 — الأوامر المتاحة:"
	@echo "  make setup      — إعداد البيئة وتثبيت المتطلبات"
	@echo "  make db-init    — تهيئة قاعدة البيانات"
	@echo "  make train      — تدريب موديل Rasa"
	@echo "  make run        — تشغيل كل الخدمات"
	@echo "  make run-actions — تشغيل Actions Server فقط"
	@echo "  make run-rasa   — تشغيل Rasa Server فقط"
	@echo "  make run-webhook — تشغيل Webhook Server فقط"
	@echo "  make test       — تشغيل اختبارات Rasa"
	@echo "  make validate   — التحقق من صحة الـ data"
	@echo "  make clean      — تنظيف ملفات الـ cache"

setup:
	@echo "📦 تثبيت المتطلبات..."
	pip install -r requirements.txt --break-system-packages
	cp -n .env.example .env || true
	mkdir -p .runtime/uploads .runtime/kb
	@echo "✅ اكتملت الإعداد — تذكر ملء .env بقيمك"

db-init:
	@echo "🗄️ تهيئة قاعدة البيانات..."
	psql $$DB_URL -f database/setup.sql
	@echo "✅ قاعدة البيانات جاهزة"

train:
	@echo "🧠 تدريب موديل Rasa Pro CALM..."
	rasa train --fixed-model-name azabot-v4
	@echo "✅ التدريب اكتمل"

validate:
	@echo "🔍 التحقق من صحة الـ data..."
	rasa data validate
	@echo "✅ البيانات سليمة"

run-actions:
	@echo "⚡ تشغيل Actions Server على :5055..."
	rasa run actions --port 5055

run-rasa:
	@echo "🤖 تشغيل Rasa Pro CALM على :5005..."
	rasa run --enable-api --cors "*" --port 5005

run-webhook:
	@echo "🌐 تشغيل Webhook Server على :8000..."
	uvicorn webhook.server:app \
		--host 0.0.0.0 \
		--port 8000 \
		--workers 2 \
		--log-level info

run:
	@echo "🚀 تشغيل كل الخدمات..."
	$(MAKE) run-actions &
	sleep 3
	$(MAKE) run-rasa &
	sleep 3
	$(MAKE) run-webhook

test:
	@echo "🧪 تشغيل اختبارات Rasa..."
	rasa test

test-chat:
	@echo "💬 اختبار محادثة سريعة..."
	curl -s -X POST http://localhost:8000/chat \
		-H "Content-Type: application/json" \
		-d '{"sender_id":"make-test","message":"مرحبا","brand":"uberfix"}' \
		| python3 -m json.tool

clean:
	@echo "🧹 تنظيف ملفات الـ cache..."
	find . -type d -name __pycache__ | xargs rm -rf
	find . -name "*.pyc" -delete
	find . -name ".rasa" -type d | xargs rm -rf 2>/dev/null || true
	@echo "✅ تم التنظيف"
