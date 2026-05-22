"""
actions/action_daftra_ops.py
=============================
عمليات دفترة المحاسبية:
- ActionDaftraSyncClient  → البحث عن العميل أو إنشاؤه في دفترة
- ActionDaftraCreateInvoice → إصدار فاتورة مرتبطة بطلب الصيانة
"""

import logging
from typing import Any, Text, Dict, List

import httpx
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from .config import DAFTRA_API_KEY, DAFTRA_BASE_URL, DB_CONFIG

logger = logging.getLogger(__name__)

# ── مساعد: بناء رابط الفاتورة ──────────────────────────────────────────────


def _invoice_url(invoice_id: Any) -> str:
    """يبني رابط عرض الفاتورة من DAFTRA_BASE_URL."""
    # DAFTRA_BASE_URL = "https://{subdomain}.daftra.com/api2"
    # رابط العرض   = "https://{subdomain}.daftra.com/invoices/view/{id}"
    base = DAFTRA_BASE_URL.rstrip("/")
    # إزالة /api2 من النهاية إن وجدت
    if base.endswith("/api2"):
        base = base[: -len("/api2")]
    return f"{base}/invoices/view/{invoice_id}"


# ── مساعد: تحديث قاعدة البيانات ────────────────────────────────────────────


def _update_request_invoice(request_id: str, invoice_id: Any, doc_url: str) -> None:
    """
    يحدّث سجل الطلب في PostgreSQL بمعرف الفاتورة ورابطها.
    [محسّن] يستخدم psycopg2 فقط هنا لأن الدالة sync — الـ action نفسه sync.
    """
    try:
        import psycopg2  # type: ignore

        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE maintenance_requests
                       SET daftra_invoice_id   = %s,
                           daftra_document_url = %s,
                           payment_status      = 'pending',
                           updated_at          = NOW()
                     WHERE id = %s
                    """,
                    (str(invoice_id), doc_url, request_id),
                )
                conn.commit()
        logger.info("Invoice %s linked to request %s", invoice_id, request_id)
    except Exception as exc:
        logger.error("DB update for invoice failed: %s", exc)


# ═══════════════════════════════════════════════════════════════════════════
#  Action 1: مزامنة العميل مع دفترة
# ═══════════════════════════════════════════════════════════════════════════


class ActionDaftraSyncClient(Action):
    """
    يبحث عن العميل برقم الهاتف في دفترة.
    إذا لم يجد العميل، يقوم بإنشائه.
    يخزن Client ID في slot لاستخدامه في الفواتير.
    """

    def name(self) -> Text:
        return "action_daftra_sync_client"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        phone = tracker.get_slot("user_phone")
        name = tracker.get_slot("user_name") or "عميل واتساب"

        if not phone:
            logger.warning("action_daftra_sync_client: user_phone slot is empty")
            return []

        if not DAFTRA_API_KEY:
            logger.warning("DAFTRA_API_KEY not configured — skipping sync")
            return []

        headers = {"apikey": DAFTRA_API_KEY, "Content-Type": "application/json"}

        try:
            with httpx.Client(timeout=10) as client:
                # 1. البحث عن عميل موجود
                search_resp = client.get(
                    f"{DAFTRA_BASE_URL}/clients",
                    headers=headers,
                    params={"phone": phone},
                )
                search_resp.raise_for_status()
                res_data = search_resp.json()

                client_id = None
                if res_data.get("code") == 200 and res_data.get("data"):
                    client_id = res_data["data"][0]["Client"]["id"]
                    logger.info("Daftra: found existing client %s", client_id)
                else:
                    # 2. إنشاء عميل جديد
                    logger.info(
                        "Daftra: client not found for phone suffix %s — creating",
                        phone[-4:],
                    )
                    create_resp = client.post(
                        f"{DAFTRA_BASE_URL}/clients",
                        headers=headers,
                        json={
                            "Client": {
                                "first_name": name,
                                "phone1": phone,
                                "notes": "تمت الإضافة تلقائياً عبر AzaBot",
                            }
                        },
                    )
                    create_resp.raise_for_status()
                    create_data = create_resp.json()
                    if create_data.get("code") == 202:
                        client_id = create_data.get("id")
                        logger.info("Daftra: created new client %s", client_id)

            if client_id:
                return [SlotSet("daftra_client_id", str(client_id))]

        except Exception as exc:
            logger.error("Daftra sync error: %s", exc)

        return []


# ═══════════════════════════════════════════════════════════════════════════
#  Action 2: إصدار فاتورة في دفترة
# ═══════════════════════════════════════════════════════════════════════════


class ActionDaftraCreateInvoice(Action):
    """
    يصدر فاتورة مسودة في دفترة بناءً على الخدمة المقدمة.
    يربط الفاتورة بطلب الصيانة في قاعدة البيانات.
    """

    def name(self) -> Text:
        return "action_daftra_create_invoice"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        client_id = tracker.get_slot("daftra_client_id")
        service_item = tracker.get_slot("service_item") or "خدمة صيانة عامة"

        if not client_id:
            logger.warning(
                "action_daftra_create_invoice: daftra_client_id is empty — "
                "run action_daftra_sync_client first"
            )
            dispatcher.utter_message(
                text="جاري مزامنة بياناتك المالية مع النظام، يرجى المحاولة مجدداً."
            )
            return []

        if not DAFTRA_API_KEY:
            logger.warning("DAFTRA_API_KEY not configured — skipping invoice creation")
            dispatcher.utter_message(
                text="⚠️ نظام الفواتير غير مضبوط حالياً، سيتم إصدار الفاتورة يدوياً."
            )
            return []

        headers = {"apikey": DAFTRA_API_KEY, "Content-Type": "application/json"}
        invoice_payload = {
            "Invoice": {
                "client_id": int(client_id),
                "draft": True,  # مسودة — يراجعها المحاسب قبل الإرسال
                "notes": "صادرة عبر AzaBot",
            },
            "InvoiceItem": [
                {
                    "item": service_item,
                    "quantity": 1,
                    "unit_price": 0,  # السعر يُحدَّد لاحقاً من المحاسب
                }
            ],
        }

        try:
            with httpx.Client(timeout=10) as client:
                resp = client.post(
                    f"{DAFTRA_BASE_URL}/invoices",
                    headers=headers,
                    json=invoice_payload,
                )
                resp.raise_for_status()
                res_data = resp.json()

            if res_data.get("code") == 202:
                invoice_id = res_data.get("id")
                doc_url = _invoice_url(invoice_id)

                # تحديث قاعدة البيانات إذا كان هناك request_id
                request_id = tracker.get_slot("maintenance_request_id")
                if request_id:
                    _update_request_invoice(request_id, invoice_id, doc_url)

                logger.info("Daftra: invoice %s created for client %s", invoice_id, client_id)
                dispatcher.utter_message(
                    text=(
                        f"✅ تم إصدار الفاتورة بنجاح.\n"
                        f"🔗 يمكنك استلامها من هنا: {doc_url}"
                    )
                )
                return [
                    SlotSet("daftra_last_invoice_id", str(invoice_id)),
                    SlotSet("daftra_document_url", doc_url),
                ]
            else:
                logger.error("Daftra invoice creation returned: %s", res_data)
                dispatcher.utter_message(
                    text="⚠️ تعذر إصدار الفاتورة آلياً، سيتم مراجعتها من قبل المحاسب."
                )

        except Exception as exc:
            logger.error("Daftra invoice error: %s", exc)
            dispatcher.utter_message(
                text="⚠️ تعذر إصدار الفاتورة آلياً، سيتم مراجعتها من قبل المحاسب."
            )

        return []
