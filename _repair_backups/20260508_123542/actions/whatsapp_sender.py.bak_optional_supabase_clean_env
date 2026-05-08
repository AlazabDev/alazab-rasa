# actions/whatsapp_sender.py
# وحدة إرسال رسائل WhatsApp باستخدام القوالب المخزنة في Supabase

import os
import json
import logging
import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime
from supabase import create_client, Client

# ============================================================================
# إعدادات التسجيل
# ============================================================================
logger = logging.getLogger(__name__)

# ============================================================================
# متغيرات البيئة
# ============================================================================
WHATSAPP_TOKEN = os.environ.get("META_TOKEN", "")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "873908352481274")
WABA_ID = os.environ.get("WABA_ID", "459851797218855")
API_VERSION = "v24.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_API_KEY", "")

# ============================================================================
# اتصال Supabase
# ============================================================================
supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("✅ Supabase connected")

# ============================================================================
# فئات البيانات (Data Classes)
# ============================================================================

class TemplateVariable:
    """متغيرات القالب"""
    def __init__(self, name: str, type: str = "text", example: str = "", required: bool = True):
        self.name = name
        self.type = type
        self.example = example
        self.required = required

class WhatsAppTemplate:
    """نموذج قالب WhatsApp"""
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("id")
        self.name = data.get("name")
        self.language = data.get("language", "ar")
        self.category = data.get("category", "UTILITY")
        self.status = data.get("status", "APPROVED")
        self.waba_id = data.get("waba_id")
        self.waba_name = data.get("waba_name")
        self.variables = data.get("variables", [])
        self.description = data.get("description", "")

    def to_dict(self) -> Dict[str, Any]:
        """تحويل الكائن إلى قاموس"""
        return {
            "id": self.id,
            "name": self.name,
            "language": self.language,
            "category": self.category,
            "status": self.status,
            "variables": self.variables,
            "description": self.description
        }

class WhatsAppMessage:
    """رسالة واتساب للإرسال"""
    def __init__(self, to: str, template_name: str, language: str = "ar", components: List[Dict] = None):
        self.to = to
        self.template_name = template_name
        self.language = language
        self.components = components or []

# ============================================================================
# دوال مساعدة للقوالب
# ============================================================================

def get_template_from_supabase(template_name: str, waba_id: str = None) -> Optional[WhatsAppTemplate]:
    """
    جلب قالب من Supabase باستخدام اسم القالب

    Args:
        template_name: اسم القالب (مثل: uberfix_request_received)
        waba_id: معرف WABA (اختياري)

    Returns:
        WhatsAppTemplate object or None
    """
    if not supabase:
        logger.error("Supabase not configured")
        return None

    try:
        query = supabase.table("whatsapp_templates").select("*").eq("name", template_name)

        if waba_id:
            query = query.eq("waba_id", waba_id)

        response = query.execute()

        if response.data and len(response.data) > 0:
            return WhatsAppTemplate(response.data[0])
        else:
            logger.warning(f"Template '{template_name}' not found in Supabase")
            return None

    except Exception as e:
        logger.error(f"Error fetching template from Supabase: {e}")
        return None


def get_all_templates(waba_id: str = None) -> List[WhatsAppTemplate]:
    """جلب جميع القوالب من Supabase"""
    if not supabase:
        logger.error("Supabase not configured")
        return []

    try:
        query = supabase.table("whatsapp_templates").select("*")

        if waba_id:
            query = query.eq("waba_id", waba_id)

        response = query.execute()

        return [WhatsAppTemplate(row) for row in response.data]

    except Exception as e:
        logger.error(f"Error fetching templates: {e}")
        return []


def create_template_components(variables: Dict[str, str]) -> List[Dict]:
    """
    إنشاء components للإرسال بناءً على المتغيرات

    Args:
        variables: قاموس المتغيرات {variable_name: value}

    Returns:
        قائمة components بصيغة Meta API
    """
    if not variables:
        return []

    body_parameters = []
    button_parameters = []

    for var_name, var_value in variables.items():
        param = {
            "type": "text",
            "text": var_value
        }
        body_parameters.append(param)

    components = []

    if body_parameters:
        components.append({
            "type": "body",
            "parameters": body_parameters
        })

    if button_parameters:
        components.append({
            "type": "button",
            "sub_type": "url",
            "index": 0,
            "parameters": button_parameters
        })

    return components


def send_whatsapp_message(message: WhatsAppMessage) -> Dict[str, Any]:
    """
    إرسال رسالة عبر WhatsApp Cloud API

    Args:
        message: كائن WhatsAppMessage

    Returns:
        استجابة من Meta API
    """
    url = f"{BASE_URL}/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": message.to,
        "type": "template",
        "template": {
            "name": message.template_name,
            "language": {
                "code": message.language
            }
        }
    }

    if message.components:
        payload["template"]["components"] = message.components

    logger.info(f"Sending WhatsApp message to {message.to}: {message.template_name}")

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"WhatsApp message sent successfully: {result.get('messages', [{}])[0].get('id')}")
            return {"success": True, "data": result}

    except httpx.HTTPStatusError as e:
        logger.error(f"WhatsApp API error: {e.response.text}")
        return {"success": False, "error": e.response.text}
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# قوالب مُعدة مسبقاً (Pre-built Templates)
# ============================================================================

class UberFixTemplates:
    """قوالب أوبرفيكس الجاهزة"""

    @staticmethod
    def request_received(to: str, order_id: str, track_url: str = None) -> WhatsAppMessage:
        """قالب: تم استلام طلب الصيانة"""
        variables = {
            "customer_name": "",
            "order_id": order_id
        }

        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": ""},
                    {"type": "text", "text": order_id}
                ]
            }
        ]

        if track_url:
            components.append({
                "type": "button",
                "sub_type": "url",
                "index": 0,
                "parameters": [{"type": "text", "text": track_url}]
            })

        return WhatsAppMessage(
            to=to,
            template_name="uberfix_request_received",
            language="ar",
            components=components
        )

    @staticmethod
    def technician_assigned(to: str, order_id: str, technician_name: str, track_url: str) -> WhatsAppMessage:
        """قالب: تم تعيين فني"""
        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": order_id},
                    {"type": "text", "text": technician_name},
                    {"type": "text", "text": track_url}
                ]
            }
        ]

        return WhatsAppMessage(
            to=to,
            template_name="technician_assigned",
            language="ar",
            components=components
        )

    @staticmethod
    def technician_on_way(to: str, track_url: str) -> WhatsAppMessage:
        """قالب: الفني في الطريق"""
        components = [
            {
                "type": "body",
                "parameters": [{"type": "text", "text": track_url}]
            },
            {
                "type": "button",
                "sub_type": "url",
                "index": 0,
                "parameters": [{"type": "text", "text": track_url}]
            }
        ]

        return WhatsAppMessage(
            to=to,
            template_name="technician_on_way",
            language="ar",
            components=components
        )

    @staticmethod
    def work_started(to: str, customer_name: str, order_id: str) -> WhatsAppMessage:
        """قالب: بدء العمل"""
        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": customer_name},
                    {"type": "text", "text": order_id}
                ]
            }
        ]

        return WhatsAppMessage(
            to=to,
            template_name="uberfix_work_started",
            language="ar",
            components=components
        )

    @staticmethod
    def work_completed(to: str, customer_name: str, order_id: str) -> WhatsAppMessage:
        """قالب: اكتمال العمل"""
        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": customer_name},
                    {"type": "text", "text": order_id}
                ]
            }
        ]

        return WhatsAppMessage(
            to=to,
            template_name="uberfix_request_completed",
            language="ar",
            components=components
        )

    @staticmethod
    def payment_received(to: str, customer_name: str, amount: str, order_id: str) -> WhatsAppMessage:
        """قالب: تأكيد استلام الدفع"""
        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": customer_name},
                    {"type": "text", "text": amount},
                    {"type": "text", "text": order_id}
                ]
            }
        ]

        return WhatsAppMessage(
            to=to,
            template_name="uberfix_request_paid",
            language="ar",
            components=components
        )


class LuxuryFinishingTemplates:
    """قوالب Luxury Finishing الجاهزة"""

    @staticmethod
    def welcome(to: str, customer_name: str) -> WhatsAppMessage:
        """قالب: ترحيب Luxury Finishing"""
        components = [
            {
                "type": "body",
                "parameters": [{"type": "text", "text": customer_name}]
            }
        ]

        return WhatsAppMessage(
            to=to,
            template_name="lux_welcome",
            language="ar",
            components=components
        )

    @staticmethod
    def inspection_request(to: str, customer_name: str) -> WhatsAppMessage:
        """قالب: طلب معاينة"""
        components = [
            {
                "type": "body",
                "parameters": [{"type": "text", "text": customer_name}]
            }
        ]

        return WhatsAppMessage(
            to=to,
            template_name="lux_inspection_request",
            language="ar",
            components=components
        )


class GeneralTemplates:
    """قوالب عامة"""

    @staticmethod
    def welcome_message(to: str, customer_name: str) -> WhatsAppMessage:
        """قالب: رسالة ترحيب عامة"""
        components = [
            {
                "type": "body",
                "parameters": [{"type": "text", "text": customer_name}]
            }
        ]

        return WhatsAppMessage(
            to=to,
            template_name="welcome_message",
            language="ar",
            components=components
        )

    @staticmethod
    def invoice_ready(to: str, customer_name: str, invoice_number: str) -> WhatsAppMessage:
        """قالب: الفاتورة جاهزة"""
        components = [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": customer_name},
                    {"type": "text", "text": invoice_number}
                ]
            }
        ]

        return WhatsAppMessage(
            to=to,
            template_name="invoice_ready",
            language="ar",
            components=components
        )


# ============================================================================
# الدوال الرئيسية للإرسال
# ============================================================================

async def send_template_message(
    to: str,
    template_name: str,
    variables: Dict[str, str],
    language: str = "ar"
) -> Dict[str, Any]:
    """
    إرسال رسالة قالب إلى واتساب

    Args:
        to: رقم الهاتف المستلم (بالصيغة الدولية: 20xxxxxxxxx)
        template_name: اسم القالب (مثل: uberfix_request_received)
        variables: قاموس المتغيرات {variable_name: value}
        language: لغة القالب (افتراضي: ar)

    Returns:
        نتيجة الإرسال
    """
    # تنسيق رقم الهاتف
    if not to.startswith("20") and not to.startswith("+"):
        to = f"20{to}"
    to = to.replace("+", "")

    # إنشاء components من المتغيرات
    components = []

    if variables:
        body_parameters = []
        button_parameters = []

        for var_name, var_value in variables.items():
            body_parameters.append({
                "type": "text",
                "text": str(var_value)
            })

        if body_parameters:
            components.append({
                "type": "body",
                "parameters": body_parameters
            })

        if button_parameters:
            components.append({
                "type": "button",
                "sub_type": "url",
                "index": 0,
                "parameters": button_parameters
            })

    # إرسال الرسالة
    message = WhatsAppMessage(
        to=to,
        template_name=template_name,
        language=language,
        components=components
    )

    return send_whatsapp_message(message)


async def send_order_confirmation(to: str, order_id: str, track_url: str = None) -> Dict[str, Any]:
    """إرسال تأكيد طلب الصيانة"""
    variables = {
        "order_id": order_id
    }
    if track_url:
        variables["track_url"] = track_url

    return await send_template_message(to, "uberfix_request_received", variables)


async def send_technician_assigned(to: str, order_id: str, technician_name: str, track_url: str) -> Dict[str, Any]:
    """إرسال إشعار تعيين فني"""
    variables = {
        "order_id": order_id,
        "technician_name": technician_name,
        "track_url": track_url
    }
    return await send_template_message(to, "technician_assigned", variables)


async def send_technician_on_way(to: str, track_url: str) -> Dict[str, Any]:
    """إرسال إشعار وصول الفني"""
    variables = {"track_url": track_url}
    return await send_template_message(to, "technician_on_way", variables)


async def send_work_started(to: str, customer_name: str, order_id: str) -> Dict[str, Any]:
    """إرسال إشعار بدء العمل"""
    variables = {
        "customer_name": customer_name,
        "order_id": order_id
    }
    return await send_template_message(to, "uberfix_work_started", variables)


async def send_work_completed(to: str, customer_name: str, order_id: str) -> Dict[str, Any]:
    """إرسال إشعار اكتمال العمل"""
    variables = {
        "customer_name": customer_name,
        "order_id": order_id
    }
    return await send_template_message(to, "uberfix_request_completed", variables)


async def send_payment_received(to: str, customer_name: str, amount: str, order_id: str) -> Dict[str, Any]:
    """إرسال إشعار استلام الدفع"""
    variables = {
        "customer_name": customer_name,
        "amount": amount,
        "order_id": order_id
    }
    return await send_template_message(to, "uberfix_request_paid", variables)


async def send_luxury_welcome(to: str, customer_name: str) -> Dict[str, Any]:
    """إرسال ترحيب Luxury Finishing"""
    variables = {"customer_name": customer_name}
    return await send_template_message(to, "lux_welcome", variables)


async def send_invoice_ready(to: str, customer_name: str, invoice_number: str) -> Dict[str, Any]:
    """إرسال إشعار جاهزية الفاتورة"""
    variables = {
        "customer_name": customer_name,
        "invoice_number": invoice_number
    }
    return await send_template_message(to, "invoice_ready", variables)


# ============================================================================
# دوال الإرسال الجماعي
# ============================================================================

async def send_bulk_messages(
    recipients: List[Dict[str, Any]],
    template_name: str,
    variables_template: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    إرسال رسائل متعددة لنفس القالب

    Args:
        recipients: قائمة المستلمين [{to: "20123456789", name: "أحمد"}]
        template_name: اسم القالب
        variables_template: قالب المتغيرات (سيتم استبدال {name} بالقيم)

    Returns:
        قائمة بنتائج الإرسال
    """
    results = []

    for recipient in recipients:
        # استبدال المتغيرات لكل مستلم
        variables = {}
        for key, value_template in variables_template.items():
            value = value_template
            for placeholder, val in recipient.items():
                value = value.replace(f"{{{placeholder}}}", str(val))
            variables[key] = value

        result = await send_template_message(
            to=recipient["to"],
            template_name=template_name,
            variables=variables
        )

        results.append({
            "to": recipient["to"],
            "success": result.get("success", False),
            "result": result
        })

    return results


# ============================================================================
# دالة اختبار
# ============================================================================

async def test_sender():
    """اختبار إرسال رسالة تجريبية"""
    test_number = os.environ.get("TEST_PHONE_NUMBER", "201004006620")

    result = await send_order_confirmation(
        to=test_number,
        order_id="TEST-001",
        track_url="https://uberfix.shop/track/test"
    )

    print(f"Test result: {result}")
    return result


# ============================================================================
# التشغيل المباشر (للاختبار)
# ============================================================================
if __name__ == "__main__":
    import asyncio

    async def main():
        logger.info("🧪 Testing WhatsApp sender...")
        result = await test_sender()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    asyncio.run(main())
