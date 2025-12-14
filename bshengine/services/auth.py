"""Authentication service"""
from typing import Optional, Any
from ..client import BshClient, BshClientFnParams
from ..types import BshResponse


class AuthService:
    """Service for authentication operations"""

    def __init__(self, client: BshClient):
        self.client = client
        self.base_endpoint = "/api/auth"

    def login(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Login user"""
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/login",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="auth.login",
            )
        )

    def register(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Register new user"""
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/register",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="auth.register",
            )
        )

    def refresh_token(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Refresh authentication token"""
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/refresh",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="auth.refreshToken",
            )
        )

    def forget_password(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Request password reset"""
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/forget-password",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="auth.forgetPassword",
            )
        )

    def reset_password(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Reset password with code"""
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/reset-password",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="auth.resetPassword",
            )
        )

    def activate_account(
        self,
        payload: dict,
        on_success: Optional[Any] = None,
        on_error: Optional[Any] = None,
    ) -> Optional[BshResponse]:
        """Activate user account"""
        return self.client.post(
            BshClientFnParams(
                path=f"{self.base_endpoint}/activate-account",
                options={
                    "response_type": "json",
                    "request_format": "json",
                    "body": payload,
                    "headers": {"Content-Type": "application/json"},
                },
                bsh_options={"on_success": on_success, "on_error": on_error},
                api="auth.activateAccount",
            )
        )

