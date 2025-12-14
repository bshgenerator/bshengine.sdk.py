"""User service"""
from typing import Optional, Any, Dict
from urllib.parse import urlencode
from ..client import BshClient, BshClientFnParams
from ..types import BshResponse, BshSearch


class UserService:
    """Service for user operations"""

    def __init__(self, client: BshClient):
        self.client = client
        self.base_endpoint = "/api/users"

    def me(
        self,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Get current user"""
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/me",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="user.me",
            )
        )

    def init(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Initialize user profile"""
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/init",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="user.init",
            )
        )

    def update_profile(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Update user profile"""
        return self.client.put(
            BshClientFnParams(
                path=f"{self.base_endpoint}/profile",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="user.updateProfile",
            )
        )

    def update_picture(
        self,
        file_path: str,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Update user picture"""
        import os
        with open(file_path, "rb") as f:
            files = {"picture": (os.path.basename(file_path), f)}
            return self.client.post(
                BshClientFnParams(
                    path=f"{self.base_endpoint}/picture",
                    options={
                        "response_type": "json",
                        "request_format": "form",
                        "body": {"files": files},
                    },
                    bsh_options={"on_success": on_success, "on_error": on_error},
                    api="user.updatePicture",
                )
            )

    def update_password(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Update user password"""
        return self.client.put(
            BshClientFnParams(
                path=f"{self.base_endpoint}/password",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="user.updatePassword",
            )
        )

    def get_by_id(
        self,
        id: str,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Get user by ID"""
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{id}",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="user.getById",
            )
        )

    def search(
        self,
        payload: BshSearch,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Search users"""
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
                api="user.search",
            )
        )

    def list(
        self,
        query_params: Optional[Dict[str, str]] = None,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """List users"""
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
                api="user.list",
            )
        )

    def update(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Update user"""
        return self.client.put(
            BshClientFnParams(
                path=self.base_endpoint,
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="user.update",
            )
        )

    def delete_by_id(
        self,
        id: str,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Delete user by ID"""
        return self.client.delete(
            BshClientFnParams(
                path=f"{self.base_endpoint}/{id}",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="user.deleteById",
            )
        )

    def count(
        self,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Count users"""
        return self.client.get(
            BshClientFnParams(
                path=f"{self.base_endpoint}/count",
                options={
                    "response_type": "json",
                    "request_format": "json",
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="user.count",
            )
        )

    def count_filtered(
        self,
        payload: BshSearch,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Count users with search criteria"""
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
                api="user.countFiltered",
            )
        )

