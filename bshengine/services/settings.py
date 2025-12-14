"""Settings service"""
from typing import Optional, Any
from ..client import BshClient, BshClientFnParams
from ..types import BshResponse


class SettingsService:
    """Service for settings operations"""

    def __init__(self, client: BshClient):
        self.client = client
        self.base_endpoint = "/api/settings"

    def load(
        self,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Load settings"""
        return self.client.get(
            BshClientFnParams(
                path=self.base_endpoint,
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="settings.load",
            )
        )

    def update(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Update settings"""
        payload_with_name = {**payload, "name": "BshEngine"}
        return self.client.put(
            BshClientFnParams(
                path=self.base_endpoint,
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload_with_name,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="settings.update",
            )
        )

