"""Typed errors for the maintenance workflow."""


class MaintenanceError(Exception):
    """Base error for expected maintenance failures."""


class MaintenanceValidationError(MaintenanceError):
    """Raised when the user request is missing required data."""

    def __init__(self, missing_fields: list[str]):
        super().__init__(", ".join(missing_fields))
        self.missing_fields = missing_fields


class MaintenanceConfigError(MaintenanceError):
    """Raised when no maintenance gateway is configured."""


class MaintenanceGatewayError(MaintenanceError):
    """Raised when the maintenance gateway rejects or fails a request."""
