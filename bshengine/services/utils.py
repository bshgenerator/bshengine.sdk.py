"""Utils service"""
from typing import Optional, Any
from ..client import BshClient, BshClientFnParams
from ..types import BshResponse


class BshUtilsService:
    """Service for utility operations"""

    def __init__(self, client: BshClient):
        self.client = client
        self.base_endpoint = "/api/utils"

    def trigger_plugins(
        self,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Get trigger plugins"""
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/triggers/plugins",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="utils.triggerPlugins",
            )
        )

    def trigger_actions(
        self,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Get trigger actions"""
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/triggers/actions",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="utils.triggerActions",
            )
        )

