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

from .config import DAFTRA_API_KEY, DAFTRA_BASE_URL
from .core.db import update as db_update

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


async def _update_request_invoice(request_id: str, invoice_id: Any, doc_url: str) -> None:
    """يحدّث طلب الصيانة في Supabase بمعلومات الفاتورة."""
    ok = await db_update(
        "maintenance_requests",
        {"id": request_id},
        {
            "daftra_invoice_id":   str(invoice_id),
            "daftra_document_url": doc_url,
            "payment_status":      "pending",
        },
    )
    if ok:
        logger.info("Invoice %s linked to request %s", invoice_id, request_id)
    else:
        logger.error("Supabase update for invoice failed: request=%s", request_id)


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


# ═══════════════════════════════════════════════════════════════════════════
#  Action 3: الاستعلام عن حالة الحساب
# ═══════════════════════════════════════════════════════════════════════════

class ActionDaftraGetAccountStatus(Action):
    def name(self) -> Text:
        return "action_daftra_get_account_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        client_id = tracker.get_slot("daftra_client_id")
        if not client_id:
            dispatcher.utter_message(text="⚠️ عذراً، لم نتمكن من تحديد حسابك في النظام المالي.")
            return []

        if not DAFTRA_API_KEY:
            dispatcher.utter_message(text="⚠️ نظام الحسابات غير متصل حالياً.")
            return []

        headers = {"apikey": DAFTRA_API_KEY, "Content-Type": "application/json"}
        try:
            with httpx.Client(timeout=10) as client:
                resp = client.get(f"{DAFTRA_BASE_URL}/clients/{client_id}", headers=headers)
                resp.raise_for_status()
                data = resp.json().get("data", {}).get("Client", {})

                balance = float(data.get("balance", 0))
                
                if balance > 0:
                    status_text = f"رصيد حسابك الحالي يوضح وجود مبلغ مستحق الدفع قدره: {balance} ريال."
                elif balance < 0:
                    status_text = f"يوجد لديك رصيد دائن قدره: {abs(balance)} ريال."
                else:
                    status_text = "رصيد حسابك الحالي مسوى ولا توجد أي مبالغ مستحقة."

                dispatcher.utter_message(text=f"📊 **حالة الحساب**\n\n{status_text}")
        except Exception as exc:
            logger.error("Daftra account status error: %s", exc)
            dispatcher.utter_message(text="⚠️ حدث خطأ أثناء الاستعلام عن حالة الحساب.")

        return []


# ═══════════════════════════════════════════════════════════════════════════
#  Action 4: الاستعلام عن آخر فاتورة
# ═══════════════════════════════════════════════════════════════════════════

class ActionDaftraGetLastInvoice(Action):
    def name(self) -> Text:
        return "action_daftra_get_last_invoice"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        client_id = tracker.get_slot("daftra_client_id")
        if not client_id:
            dispatcher.utter_message(text="⚠️ عذراً، لم نتمكن من تحديد حسابك.")
            return []

        headers = {"apikey": DAFTRA_API_KEY, "Content-Type": "application/json"}
        try:
            with httpx.Client(timeout=10) as client:
                # نجلب أحدث الفواتير الخاصة بالعميل
                resp = client.get(
                    f"{DAFTRA_BASE_URL}/invoices",
                    headers=headers,
                    params={"client_id": client_id, "limit": 1}
                )
                resp.raise_for_status()
                invoices = resp.json().get("data", [])

                if not invoices:
                    dispatcher.utter_message(text="لم يتم العثور على فواتير سابقة لحسابك.")
                    return []

                inv = invoices[0].get("Invoice", {})
                inv_id = inv.get("id")
                amount = inv.get("total", "غير محدد")
                doc_url = _invoice_url(inv_id)

                status_map = {"1": "مسودة", "2": "غير مدفوعة", "3": "مدفوعة", "4": "مدفوعة جزئياً"}
                payment_status = status_map.get(str(inv.get("status")), "غير معروف")

                dispatcher.utter_message(
                    text=f"🧾 **تفاصيل آخر فاتورة**\n"
                         f"رقم الفاتورة: {inv_id}\n"
                         f"القيمة الإجمالية: {amount}\n"
                         f"الحالة: {payment_status}\n\n"
                         f"🔗 لعرض الفاتورة وتحميلها: {doc_url}"
                )
        except Exception as exc:
            logger.error("Daftra get invoice error: %s", exc)
            dispatcher.utter_message(text="⚠️ حدث خطأ أثناء جلب تفاصيل الفاتورة.")

        return []


# ═══════════════════════════════════════════════════════════════════════════
#  Action 5: الاستعلام عن حالة المشروع (أمر الشغل)
# ═══════════════════════════════════════════════════════════════════════════

class ActionDaftraGetProjectStatus(Action):
    def name(self) -> Text:
        return "action_daftra_get_project_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        client_id = tracker.get_slot("daftra_client_id")
        if not client_id:
            dispatcher.utter_message(text="⚠️ لم يتم العثور على حساب مرتبط للاستعلام عن المشاريع.")
            return []

        headers = {"apikey": DAFTRA_API_KEY, "Content-Type": "application/json"}
        try:
            with httpx.Client(timeout=10) as client:
                # نستعلم عن أوامر الشغل الخاصة بالعميل (التي تمثل المشاريع)
                resp = client.get(
                    f"{DAFTRA_BASE_URL}/work_orders",
                    headers=headers,
                    params={"client_id": client_id, "limit": 1}
                )
                resp.raise_for_status()
                work_orders = resp.json().get("data", [])

                if not work_orders:
                    dispatcher.utter_message(text="لا توجد مشاريع أو أوامر شغل مسجلة في حسابك حالياً.")
                    return []

                wo = work_orders[0].get("WorkOrder", {})
                wo_no = wo.get("number", wo.get("id"))
                status_id = str(wo.get("status", ""))
                
                # حالات افتراضية شائعة لأوامر الشغل في دفترة
                status_map = {
                    "1": "مسودة (Draft)", 
                    "2": "جاري التنفيذ (In Progress)", 
                    "3": "مكتمل (Completed)",
                    "4": "ملغي (Cancelled)",
                    "5": "قيد المراجعة (Under Review)"
                }
                status_text = status_map.get(status_id, "قيد المعالجة")

                dispatcher.utter_message(
                    text=f"🏗️ **حالة آخر مشروع / أمر شغل**\n"
                         f"رقم المشروع: {wo_no}\n"
                         f"الحالة الحالية: {status_text}"
                )
        except Exception as exc:
            logger.error("Daftra get work order error: %s", exc)
            dispatcher.utter_message(text="⚠️ تعذر جلب حالة المشروع حالياً، يرجى المحاولة لاحقاً.")

        return []
