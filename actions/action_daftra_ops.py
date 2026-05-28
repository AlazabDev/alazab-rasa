"""
actions/action_daftra_ops.py
=============================
Daftra accounting actions for AzaBot.

Production scope:
- action_daftra_sync_client: find/create Daftra client by phone.
- action_daftra_create_invoice: create draft invoice and link it to maintenance request.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Text

import httpx
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from .config import DAFTRA_API_KEY, DAFTRA_BASE_URL
from .core.db import update as db_update

logger = logging.getLogger(__name__)


def _clean(value: Any) -> str:
    return str(value or "").strip()


def _invoice_url(invoice_id: Any) -> str:
    """Build public Daftra invoice URL from configured API base URL."""
    base = DAFTRA_BASE_URL.rstrip("/")
    if base.endswith("/api2"):
        base = base[: -len("/api2")]
    return f"{base}/invoices/view/{invoice_id}"


def _headers() -> dict[str, str]:
    return {"apikey": DAFTRA_API_KEY, "Content-Type": "application/json"}


def _extract_client_id(payload: dict[str, Any]) -> Optional[str]:
    """Handle common Daftra API response shapes."""
    if payload.get("id"):
        return str(payload["id"])

    data = payload.get("data")
    if isinstance(data, list) and data:
        first = data[0]
        if isinstance(first, dict):
            client = first.get("Client") if isinstance(first.get("Client"), dict) else first
            if client.get("id"):
                return str(client["id"])

    if isinstance(data, dict):
        client = data.get("Client") if isinstance(data.get("Client"), dict) else data
        if client.get("id"):
            return str(client["id"])

    return None


async def _update_request_invoice(request_id: str, invoice_id: Any, doc_url: str) -> bool:
    """Link created invoice to the maintenance request in Supabase."""
    request_id = _clean(request_id)
    if not request_id:
        return False

    ok = await db_update(
        "maintenance_requests",
        {"id": request_id},
        {
            "daftra_invoice_id": str(invoice_id),
            "daftra_document_url": doc_url,
            "payment_status": "pending",
        },
    )
    if ok:
        logger.info("Invoice %s linked to request %s", invoice_id, request_id)
    else:
        logger.error("Supabase update for invoice failed: request=%s", request_id)
    return ok


class ActionDaftraSyncClient(Action):
    """Find Daftra client by phone, or create it when missing."""

    def name(self) -> Text:
        return "action_daftra_sync_client"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        phone = _clean(tracker.get_slot("user_phone") or tracker.get_slot("maintenance_client_phone"))
        name = _clean(tracker.get_slot("user_name") or tracker.get_slot("maintenance_client_name")) or "عميل واتساب"

        if not phone:
            logger.warning("action_daftra_sync_client: user phone slot is empty")
            return []

        if not DAFTRA_API_KEY:
            logger.warning("DAFTRA_API_KEY not configured — skipping sync")
            return []

        client_id: Optional[str] = None

        try:
            async with httpx.AsyncClient(timeout=15) as client:
                search_resp = await client.get(
                    f"{DAFTRA_BASE_URL}/clients",
                    headers=_headers(),
                    params={"phone": phone},
                )
                search_resp.raise_for_status()
                client_id = _extract_client_id(search_resp.json())

                if not client_id:
                    logger.info(
                        "Daftra: client not found for phone suffix %s — creating",
                        phone[-4:],
                    )
                    create_resp = await client.post(
                        f"{DAFTRA_BASE_URL}/clients",
                        headers=_headers(),
                        json={
                            "Client": {
                                "first_name": name,
                                "phone1": phone,
                                "notes": "تمت الإضافة تلقائياً عبر AzaBot",
                            }
                        },
                    )
                    create_resp.raise_for_status()
                    client_id = _extract_client_id(create_resp.json())

            if client_id:
                logger.info("Daftra: synced client %s", client_id)
                return [SlotSet("daftra_client_id", client_id)]

            logger.warning("Daftra: client sync returned no client id")

        except Exception as exc:
            logger.error("Daftra sync error: %s", exc)

        return []


class ActionDaftraCreateInvoice(Action):
    """Create a draft Daftra invoice and link it to the active maintenance request."""

    def name(self) -> Text:
        return "action_daftra_create_invoice"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        client_id = _clean(tracker.get_slot("daftra_client_id"))
        service_item = _clean(tracker.get_slot("service_item")) or _clean(
            tracker.get_slot("maintenance_service_type")
        ) or "خدمة صيانة عامة"

        request_id = _clean(
            tracker.get_slot("maintenance_request_id")
            or tracker.get_slot("order_id")
            or tracker.get_slot("maintenance_request_number")
            or tracker.get_slot("order_number")
        )

        if not client_id:
            logger.warning(
                "action_daftra_create_invoice: daftra_client_id is empty — run action_daftra_sync_client first"
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

        invoice_payload = {
            "Invoice": {
                "client_id": int(client_id),
                "draft": True,
                "notes": "صادرة عبر AzaBot",
            },
            "InvoiceItem": [
                {
                    "item": service_item,
                    "quantity": 1,
                    "unit_price": 0,
                }
            ],
        }

        try:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.post(
                    f"{DAFTRA_BASE_URL}/invoices",
                    headers=_headers(),
                    json=invoice_payload,
                )
                resp.raise_for_status()
                res_data = resp.json()

            invoice_id = res_data.get("id") or _extract_client_id(res_data)
            if not invoice_id:
                logger.error("Daftra invoice creation returned no invoice id: %s", res_data)
                dispatcher.utter_message(
                    text="⚠️ تعذر إصدار الفاتورة آلياً، سيتم مراجعتها من قبل المحاسب."
                )
                return []

            doc_url = _invoice_url(invoice_id)
            linked = False
            if request_id:
                linked = await _update_request_invoice(request_id, invoice_id, doc_url)

            logger.info(
                "Daftra: invoice %s created for client %s | linked=%s",
                invoice_id,
                client_id,
                linked,
            )

            dispatcher.utter_message(
                text=(
                    "✅ تم إصدار الفاتورة بنجاح.\n"
                    f"🔗 يمكنك استلامها من هنا: {doc_url}"
                )
            )

            events: List[Dict[Text, Any]] = [
                SlotSet("daftra_last_invoice_id", str(invoice_id)),
                SlotSet("daftra_document_url", doc_url),
            ]
            if linked:
                events.append(SlotSet("payment_status", "pending"))
            return events

        except Exception as exc:
            logger.error("Daftra invoice error: %s", exc)
            dispatcher.utter_message(
                text="⚠️ تعذر إصدار الفاتورة آلياً، سيتم مراجعتها من قبل المحاسب."
            )
            return []
