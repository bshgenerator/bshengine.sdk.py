"""API Key service"""
from typing import Optional, Any, Dict
from urllib.parse import urlencode
from ..client import BshClient, BshClientFnParams
from ..types import BshResponse, BshSearch


class ApiKeyService:
    """Service for API key operations"""

    def __init__(self, client: BshClient):
        self.client = client
        self.base_endpoint = "/api/api-keys"

    def create(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Create API key"""
        return self.client.post(
            BshClientFnParams(
                path=self.base_endpoint,
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="api-key.create",
            )
        )

    def details(
        self,
        id: int,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Get API key details"""
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{id}",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="api-key.details",
            )
        )

    def revoke(
        self,
        id: int,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Revoke API key"""
        return self.client.delete(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{id}/revoke",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="api-key.revoke",
            )
        )

    def get_by_id(
        self,
        id: str,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Get API key by ID"""
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{id}",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="api-key.getById",
            )
        )

    def search(
        self,
        payload: BshSearch,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Search API keys"""
        search_dict = payload.to_dict() if hasattr(payload, "to_dict") else payload
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/search",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": search_dict,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="api-key.search",
            )
        )

    def list(
        self,
        query_params: Optional[Dict[str, str]] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """List API keys"""
        endpoint = self.base_endpoint
        if query_params:
            endpoint += "?" + urlencode(query_params)
        
        return self.client.get(
            BshClientFnParams(
                path=endpoint,
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="api-key.list",
            )
        )

    def delete_by_id(
        self,
        id: str,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Delete API key by ID"""
        return self.client.delete(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{id}",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="api-key.deleteById",
            )
        )

    def count(
        self,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Count API keys"""
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/count",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="api-key.count",
            )
        )

    def count_filtered(
        self,
        payload: BshSearch,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Count API keys with search criteria"""
        search_dict = payload.to_dict() if hasattr(payload, "to_dict") else payload
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/count",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": search_dict,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="api-key.countFiltered",
            )
        )

