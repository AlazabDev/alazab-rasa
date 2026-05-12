import requests
import logging
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from .config import DAFTRA_API_KEY, DAFTRA_BASE_URL, DB_CONFIG
import psycopg2

logger = logging.getLogger(__name__)

class ActionDaftraSyncClient(Action):
    """
    يبحث عن العميل برقم الهاتف في دفترة.
    إذا لم يجد العميل، يقوم بإنشائه.
    يخزن Client ID في slot لاستخدامه في الفواتير.
    """
    def name(self) -> Text:
        return "action_daftra_sync_client"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        phone = tracker.get_slot("user_phone")
        name = tracker.get_slot("user_name") or "عميل واتساب"
        
        if not phone:
            return []

        headers = {"apikey": DAFTRA_API_KEY, "Content-Type": "application/json"}
        
        try:
            # 1. Search for existing client
            search_url = f"{DAFTRA_BASE_URL}/clients?phone={phone}"
            response = requests.get(search_url, headers=headers, timeout=10)
            res_data = response.json()
            
            client_id = None
            if res_data.get("code") == 200 and res_data.get("data"):
                # Client exists
                client_id = res_data["data"][0]["Client"]["id"]
                logger.info(f"Daftra: Found existing client {client_id}")
            else:
                # 2. Create new client
                logger.info(f"Daftra: Client not found, creating new one for {phone}")
                create_url = f"{DAFTRA_BASE_URL}/clients"
                client_payload = {
                    "Client": {
                        "first_name": name,
                        "phone1": phone,
                        "notes": "تمت الإضافة تلقائياً عبر AzaBot"
                    }
                }
                create_res = requests.post(create_url, json=client_payload, headers=headers, timeout=10)
                create_data = create_res.json()
                if create_data.get("code") == 202:
                    client_id = create_data.get("id")
                    logger.info(f"Daftra: Created new client {client_id}")

            if client_id:
                return [SlotSet("daftra_client_id", client_id)]
            
        except Exception as e:
            logger.error(f"Daftra Sync Error: {str(e)}")
            
        return []

class ActionDaftraCreateInvoice(Action):
    """
    يصدر فاتورة في دفترة بناءً على الخدمة المقدمة.
    """
    def name(self) -> Text:
        return "action_daftra_create_invoice"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        client_id = tracker.get_slot("daftra_client_id")
        service_item = tracker.get_slot("service_item") or "خدمة صيانة عامة"
        
        if not client_id:
            # Try to sync client first if ID is missing
            dispatcher.utter_message(text="جاري مزامنة بياناتك المالية مع النظام...")
            return []

        headers = {"apikey": DAFTRA_API_KEY, "Content-Type": "application/json"}
        invoice_url = f"{DAFTRA_BASE_URL}/invoices"
        
        invoice_payload = {
            "Invoice": {
                "client_id": client_id,
                "notes": "صادرة عبر AzaBot"
            },
            "InvoiceItem": [
                {
                    "item": service_item,
                    "quantity": 1,
                    "unit_price": 0 # السعر يحدد لاحقاً أو من قاعدة البيانات
                }
            ]
        }
        
        try:
            response = requests.post(invoice_url, json=invoice_payload, headers=headers, timeout=10)
            res_data = response.json()
            if res_data.get("code") == 202:
                invoice_id = res_data.get("id")
                # In production, Daftra might provide a direct link or we construct it
                document_url = f"{DAFTRA_BASE_URL.replace('/api/', '/')}/invoices/view/{invoice_id}"
                
                # Update our database to sync with Daftra
                request_id = tracker.get_slot("maintenance_request_id")
                if request_id:
                    with psycopg2.connect(**DB_CONFIG) as conn:
                        with conn.cursor() as cur:
                            cur.execute(
                                "UPDATE maintenance_requests SET daftra_invoice_id = %s, daftra_document_url = %s, payment_status = 'pending' WHERE id = %s",
                                (str(invoice_id), document_url, request_id)
                            )
                            conn.commit()

                dispatcher.utter_message(text=f"✅ تم إصدار الفاتورة بنجاح.\n🔗 يمكنك استلامها من هنا: {document_url}")
                return [SlotSet("daftra_last_invoice_id", invoice_id), SlotSet("daftra_document_url", document_url)]
        except Exception as e:
            logger.error(f"Daftra Invoice Error: {str(e)}")
            dispatcher.utter_message(text="⚠️ تعذر إصدار الفاتورة آلياً، سيتم مراجعتها من قبل المحاسب.")
            
        return []
