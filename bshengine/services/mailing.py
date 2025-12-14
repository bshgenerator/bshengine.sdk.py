"""Mailing service"""
from typing import Optional, Any
from ..client import BshClient, BshClientFnParams
from ..types import BshResponse


class MailingService:
    """Service for mailing operations"""

    def __init__(self, client: BshClient):
        self.client = client
        self.base_endpoint = "/api/mailing"

    def send(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Send email"""
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/send",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="mailing.send",
            )
        )

