from __future__ import annotations

import asyncio
import importlib.util
import json
import sys
import types
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAINTENANCE_DIR = ROOT / "actions" / "maintenance"


def load_module(name: str, path: Path) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def bootstrap_package() -> None:
    actions_pkg = types.ModuleType("actions")
    actions_pkg.__path__ = [str(ROOT / "actions")]
    sys.modules.setdefault("actions", actions_pkg)

    maintenance_pkg = types.ModuleType("actions.maintenance")
    maintenance_pkg.__path__ = [str(MAINTENANCE_DIR)]
    sys.modules.setdefault("actions.maintenance", maintenance_pkg)


class FakeDispatcher:
    def __init__(self) -> None:
        self.messages: list[dict[str, Any]] = []

    def utter_message(self, **kwargs: Any) -> None:
        self.messages.append(kwargs)


class FakeTracker:
    def __init__(self, slots: dict[str, Any], text: str) -> None:
        self._slots = slots
        self.latest_message = {"text": text}
        self.sender_id = "smoke-user"

    def get_slot(self, name: str) -> Any:
        return self._slots.get(name)


class FakeGatewayClient:
    def __init__(self) -> None:
        self.payloads: list[Any] = []
        self.idempotency_keys: list[str] = []

    async def create_request(self, payload: Any, idempotency_key: str) -> dict[str, Any]:
        self.payloads.append(payload)
        self.idempotency_keys.append(idempotency_key)
        return {
            "success": True,
            "request_id": "cfc272e9-ad9c-4d82-878d-d90940139246",
            "request_number": "AZ-UF-26-04-001056",
            "track_url": "https://uberfix.shop/track/cfc272e9-ad9c-4d82-878d-d90940139246",
            "channel": "api",
        }

    async def track_request(self, ticket: str) -> dict[str, Any]:
        return {
            "success": True,
            "request_number": ticket,
            "status": "received",
            "track_url": f"https://uberfix.shop/track/{ticket}",
        }


async def run_service_smoke() -> dict[str, Any]:
    bootstrap_package()
    load_module("actions.maintenance.errors", MAINTENANCE_DIR / "errors.py")
    schemas = load_module("actions.maintenance.schemas", MAINTENANCE_DIR / "schemas.py")
    load_module("actions.maintenance.responses", MAINTENANCE_DIR / "responses.py")
    service_module = load_module("actions.maintenance.service", MAINTENANCE_DIR / "service.py")

    normalized_phone = schemas.normalize_egyptian_phone("0100 400 6620")
    if normalized_phone != "01004006620":
        raise AssertionError(f"Phone normalization failed: {normalized_phone}")

    service_type = schemas.infer_service_type("في ماس كهرباء في فرع أبوعوف")
    if service_type != "electrical":
        raise AssertionError(f"Service inference failed: {service_type}")

    priority = schemas.infer_priority("عاجل جدا ماس كهرباء")
    if priority != "high":
        raise AssertionError(f"Priority inference failed: {priority}")

    gateway = FakeGatewayClient()
    service = service_module.MaintenanceService(gateway_client=gateway)

    dispatcher = FakeDispatcher()
    tracker = FakeTracker(
        slots={
            "name": "أحمد عزب - فرع أبوعوف",
            "phone": "01004006620",
            "service_type": None,
            "priority": None,
            "description": None,
            "branch": None,
        },
        text="طلب الصيانة لفرع ابوعوف كهرباء عاجل",
    )

    await service.create_request(dispatcher, tracker, domain={})

    if not gateway.payloads:
        raise AssertionError("Gateway was not called")

    payload = gateway.payloads[0]
    if payload.client_phone != "01004006620":
        raise AssertionError(f"Unexpected phone: {payload.client_phone}")
    if payload.service_type != "electrical":
        raise AssertionError(f"Unexpected service_type: {payload.service_type}")
    if payload.priority != "high":
        raise AssertionError(f"Unexpected priority: {payload.priority}")
    if not gateway.idempotency_keys or len(gateway.idempotency_keys[0]) < 16:
        raise AssertionError("Idempotency key was not generated")

    if not dispatcher.messages:
        raise AssertionError("Bot response was not emitted")

    response = dispatcher.messages[0]
    text = response.get("text", "")
    buttons = response.get("buttons", [])

    if "AZ-UF-26-04-001056" not in text:
        raise AssertionError(f"Request number missing from response: {text}")

    tracking_buttons = [
        button
        for button in buttons
        if "تتبع" in str(button.get("title", "")) and button.get("url")
    ]
    if not tracking_buttons:
        raise AssertionError(f"Tracking button missing: {buttons}")

    track_url = tracking_buttons[0]["url"]
    if track_url != "https://uberfix.shop/track/cfc272e9-ad9c-4d82-878d-d90940139246":
        raise AssertionError(f"Unexpected track_url: {track_url}")

    return {
        "ok": True,
        "request_number_in_response": True,
        "tracking_button_in_response": True,
        "normalized_phone": payload.client_phone,
        "service_type": payload.service_type,
        "priority": payload.priority,
        "idempotency_key_prefix": gateway.idempotency_keys[0][:12],
    }


def main() -> int:
    result = asyncio.run(run_service_smoke())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
