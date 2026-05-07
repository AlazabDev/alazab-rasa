"""User-facing responses for maintenance workflows."""

from __future__ import annotations

from typing import Any

from .schemas import MaintenanceTicket


def create_success(ticket: MaintenanceTicket) -> dict[str, Any]:
    request_number = ticket.display_number
    text = (
        "✅ تم تسجيل طلب الصيانة بنجاح!\n"
        f"رقم طلبك: *{request_number}*\n"
    )
    if ticket.track_url:
        text += f"رابط التتبع: {ticket.track_url}\n"
    text += "سيتواصل معك الفني في أقرب وقت."

    buttons: list[dict[str, str]] = []
    if request_number:
        buttons.append({"title": request_number, "payload": request_number})
    if ticket.track_url:
        buttons.append({"title": "تتبع الطلب", "url": ticket.track_url})
    return {"text": text, "buttons": buttons}


def missing_fields(missing: list[str]) -> dict[str, Any]:
    labels = {
        "phone": "رقم الهاتف",
        "description": "وصف العطل أو الخدمة المطلوبة",
    }
    readable = " و".join(labels.get(item, item) for item in missing)
    return {
        "text": (
            f"أحتاج {readable} قبل تسجيل طلب الصيانة.\n"
            "اكتب البيانات في رسالة واحدة مثل: الاسم، رقم الهاتف، الفرع، ونوع المشكلة."
        ),
        "buttons": [],
    }


def create_failed() -> dict[str, Any]:
    return {
        "text": (
            "لم أتمكن من تسجيل طلب الصيانة الآن بسبب مشكلة في بوابة الصيانة.\n"
            "احتفظت ببيانات الطلب داخل المحادثة، حاول مرة أخرى بعد لحظات أو اطلب التحويل لموظف."
        ),
        "buttons": [],
    }


def not_configured() -> dict[str, Any]:
    return {
        "text": (
            "نظام تسجيل طلبات الصيانة غير مضبوط على الخادم حاليًا.\n"
            "اضبط MAINTENANCE_GATEWAY_URL أو UBERFIX_API_URL ثم أعد المحاولة."
        ),
        "buttons": [],
    }


def track_prompt() -> dict[str, Any]:
    return {
        "text": "من فضلك أرسل رقم الطلب الذي وصلك في رسالة التأكيد وسأتحقق من حالته فورًا.",
        "buttons": [],
    }


def track_result(order_id: str, status_text: str) -> dict[str, Any]:
    return {
        "text": f"📋 طلب *{order_id}*: {status_text}",
        "buttons": [],
    }


def subscriptions() -> dict[str, Any]:
    plans = [
        ("🥉 باقة أساسية", 4, "لا", "مناسبة للمنازل والوحدات الصغيرة"),
        ("🥈 باقة متقدمة", 8, "نعم", "مناسبة للمحلات والمكاتب"),
        ("🥇 باقة بريميوم", 12, "نعم", "مناسبة للمنشآت الكبيرة والمصانع"),
    ]
    text = "🔧 *باقات UberFix السنوية:*\n\n"
    for name, visits, priority, desc in plans:
        text += (
            f"{name}\n"
            f"  زيارات: {visits} × سنويًا | أولوية: {priority}\n"
            f"  {desc}\n\n"
        )
    text += "للاشتراك أو الاستفسار عن الأسعار، تواصل معنا الآن."
    return {"text": text, "buttons": []}
