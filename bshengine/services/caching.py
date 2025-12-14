"""Caching service"""
from typing import Optional, Any
from ..client import BshClient, BshClientFnParams
from ..types import BshResponse, BshSearch


class CachingService:
    """Service for caching operations"""

    def __init__(self, client: BshClient):
        self.client = client
        self.base_endpoint = "/api/caching"

    def find_by_id(
        self,
        id: str,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Get cache by ID"""
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{id}",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="caching.findById",
            )
        )

    def search(
        self,
        payload: BshSearch,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Search caches"""
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
                api="caching.search",
            )
        )

    def names(
        self,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Get cache names"""
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/names",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="caching.names",
            )
        )

    def clear_by_id(
        self,
        id: str,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Clear cache by ID"""
        return self.client.delete(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{id}",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="caching.clearById",
            )
        )

    def clear_all(
        self,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Clear all caches"""
        return self.client.delete(
            BshClientFnParams(
                path=f"{self.base_endpoint}/all",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="caching.clearAll",
            )
        )

