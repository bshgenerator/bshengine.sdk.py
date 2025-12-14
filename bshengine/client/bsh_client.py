"""BSH Client for making HTTP requests"""
import json
import base64
from typing import Optional, Any, Dict, Callable, List
import requests
from ..types import BshResponse, BshError, is_ok, AuthToken
from .types import (
    BshClientFn,
    BshAuthFn,
    BshRefreshTokenFn,
    BshPostInterceptor,
    BshPreInterceptor,
    BshErrorInterceptor,
)


class BshClientFnParams:
    """Parameters for client function calls"""
    def __init__(
        self,
        path: str,
        options: Dict[str, Any],
        bsh_options: Dict[str, Any],
        api: Optional[str] = None,
    ):
        self.path = path
        self.options = options
        self.bsh_options = bsh_options
        self.api = api


def default_client_fn(params: BshClientFnParams) -> requests.Response:
    """Default HTTP client function using requests"""
    method = params.options.get("method", "GET")
    url = params.path
    headers = params.options.get("headers", {})
    body = params.options.get("body")
    
    # Handle form data
    if params.options.get("request_format") == "form":
        # body should be a dict with "files" and "data" keys
        if isinstance(body, dict):
            files = body.get("files")
            data = body.get("data", {})
            # Remove Content-Type header for multipart/form-data
            headers.pop("Content-Type", None)
            return requests.request(method, url, headers=headers, files=files, data=data)
        return requests.request(method, url, headers=headers, data=body)
    
    # Handle JSON
    json_data = None
    if body and params.options.get("request_format") != "form":
        if isinstance(body, dict):
            json_data = body
        else:
            json_data = body
    
    return requests.request(method, url, headers=headers, json=json_data)


class BshClient:
    """HTTP client for BSH Engine API"""

    def __init__(
        self,
        host: Optional[str] = None,
        http_client: Optional[BshClientFn] = None,
        auth_fn: Optional[BshAuthFn] = None,
        refresh_token_fn: Optional[BshRefreshTokenFn] = None,
        bsh_engine: Optional[Any] = None,
    ):
        self.host = host or ""
        self.http_client = http_client or default_client_fn
        self.auth_fn = auth_fn
        self.refresh_token_fn = refresh_token_fn
        self.bsh_engine = bsh_engine

    def _handle_response(
        self,
        response: requests.Response,
        params: BshClientFnParams,
        response_type: str = "json",
    ) -> Optional[Any]:
        """Handle HTTP response"""
        if not response.ok:
            try:
                error_data = response.json()
                bsh_response = BshResponse.from_dict(error_data)
            except:
                bsh_response = None
            
            error = BshError(response.status_code, params.path, bsh_response)
            
            # Apply error interceptors
            if self.bsh_engine and self.bsh_engine.get_error_interceptors():
                for interceptor in self.bsh_engine.get_error_interceptors():
                    new_error = interceptor(error, bsh_response, params)
                    if new_error:
                        error = new_error
            
            if params.bsh_options.get("on_error"):
                params.bsh_options["on_error"](error)
                return None
            else:
                raise error

        if response_type == "json":
            try:
                data = response.json()
                bsh_response = BshResponse.from_dict(data)
            except:
                bsh_response = BshResponse(
                    data=[response.text],
                    timestamp=0,
                    code=response.status_code,
                    status="ok",
                )
            
            if params.bsh_options.get("on_success"):
                params.bsh_options["on_success"](bsh_response)
                return None
            
            bsh_response.api = params.api
            
            # Apply post interceptors
            if self.bsh_engine and self.bsh_engine.get_post_interceptors():
                for interceptor in self.bsh_engine.get_post_interceptors():
                    new_result = interceptor(bsh_response, params)
                    if new_result:
                        bsh_response = new_result
            
            return bsh_response
        
        elif response_type == "blob":
            blob = response.content
            if params.bsh_options.get("on_download"):
                params.bsh_options["on_download"](blob)
                return None
            return blob
        
        return None

    async def _refresh_token_if_needed(
        self,
        auth: Optional[AuthToken],
    ) -> Optional[AuthToken]:
        """Refresh JWT token if needed"""
        if not self.refresh_token_fn or not auth or auth.type != "JWT":
            return auth
        
        try:
            # Decode JWT token to check expiration
            token_parts = auth.token.split(".")
            if len(token_parts) < 2:
                return auth
            
            payload = json.loads(base64.urlsafe_b64decode(token_parts[1] + "=="))
            exp = payload.get("exp", 0) * 1000
            import time
            now = int(time.time() * 1000)
            
            if exp and now < exp:
                return auth
            
            # Token expired, refresh it
            refresh_token = self.refresh_token_fn()
            if not refresh_token or not self.bsh_engine:
                return auth
            
            refresh_response = self.bsh_engine.auth.refresh_token({
                "payload": {"refresh": refresh_token},
                "on_error": lambda e: None,
            })
            
            if refresh_response and refresh_response.data:
                return AuthToken("JWT", refresh_response.data[0].get("access", auth.token))
            
            return auth
        except:
            return auth

    def _get_auth_headers(self, params: BshClientFnParams) -> Dict[str, str]:
        """Get authentication headers"""
        if "/api/auth/" in params.path:
            return {}
        
        auth = None
        if self.auth_fn:
            auth_result = self.auth_fn()
            if isinstance(auth_result, AuthToken):
                auth = auth_result
            elif isinstance(auth_result, dict):
                auth = AuthToken.from_dict(auth_result)
            elif auth_result is not None:
                # Handle tuple or other formats
                if isinstance(auth_result, (tuple, list)) and len(auth_result) == 2:
                    auth = AuthToken(type=auth_result[0], token=auth_result[1])
        
        auth_headers = {}
        if auth:
            if auth.type == "JWT":
                auth_headers["Authorization"] = f"Bearer {auth.token}"
            elif auth.type == "APIKEY":
                auth_headers["X-BSH-APIKEY"] = auth.token
        
        return auth_headers

    def _apply_pre_interceptors(self, params: BshClientFnParams) -> BshClientFnParams:
        """Apply pre-request interceptors"""
        if not self.bsh_engine or not self.bsh_engine.get_pre_interceptors():
            return params
        
        for interceptor in self.bsh_engine.get_pre_interceptors():
            new_params = interceptor(params)
            if new_params:
                return new_params
        
        return params

    def get(self, params: BshClientFnParams) -> Optional[BshResponse]:
        """Make GET request"""
        auth_headers = self._get_auth_headers(params)
        
        client_params = BshClientFnParams(
            path=f"{self.host}{params.path}",
            options={
                **params.options,
                "method": "GET",
                "headers": {
                    **params.options.get("headers", {}),
                    **auth_headers,
                },
            },
            bsh_options=params.bsh_options,
            api=params.api,
        )
        
        client_params = self._apply_pre_interceptors(client_params)
        response = self.http_client(client_params)
        return self._handle_response(response, client_params, "json")

    def post(self, params: BshClientFnParams) -> Optional[BshResponse]:
        """Make POST request"""
        auth_headers = self._get_auth_headers(params)
        
        client_params = BshClientFnParams(
            path=f"{self.host}{params.path}",
            options={
                **params.options,
                "method": "POST",
                "headers": {
                    **params.options.get("headers", {}),
                    **auth_headers,
                },
            },
            bsh_options=params.bsh_options,
            api=params.api,
        )
        
        client_params = self._apply_pre_interceptors(client_params)
        response = self.http_client(client_params)
        return self._handle_response(response, client_params, "json")

    def put(self, params: BshClientFnParams) -> Optional[BshResponse]:
        """Make PUT request"""
        auth_headers = self._get_auth_headers(params)
        
        client_params = BshClientFnParams(
            path=f"{self.host}{params.path}",
            options={
                **params.options,
                "method": "PUT",
                "headers": {
                    **params.options.get("headers", {}),
                    **auth_headers,
                },
            },
            bsh_options=params.bsh_options,
            api=params.api,
        )
        
        client_params = self._apply_pre_interceptors(client_params)
        response = self.http_client(client_params)
        return self._handle_response(response, client_params, "json")

    def delete(self, params: BshClientFnParams) -> Optional[BshResponse]:
        """Make DELETE request"""
        auth_headers = self._get_auth_headers(params)
        
        client_params = BshClientFnParams(
            path=f"{self.host}{params.path}",
            options={
                **params.options,
                "method": "DELETE",
                "headers": {
                    **params.options.get("headers", {}),
                    **auth_headers,
                },
            },
            bsh_options=params.bsh_options,
            api=params.api,
        )
        
        client_params = self._apply_pre_interceptors(client_params)
        response = self.http_client(client_params)
        return self._handle_response(response, client_params, "json")

    def patch(self, params: BshClientFnParams) -> Optional[BshResponse]:
        """Make PATCH request"""
        auth_headers = self._get_auth_headers(params)
        
        client_params = BshClientFnParams(
            path=f"{self.host}{params.path}",
            options={
                **params.options,
                "method": "PATCH",
                "headers": {
                    **params.options.get("headers", {}),
                    **auth_headers,
                },
            },
            bsh_options=params.bsh_options,
            api=params.api,
        )
        
        client_params = self._apply_pre_interceptors(client_params)
        response = self.http_client(client_params)
        return self._handle_response(response, client_params, "json")

    def download(self, params: BshClientFnParams) -> Optional[bytes]:
        """Download file as blob"""
        auth_headers = self._get_auth_headers(params)
        
        client_params = BshClientFnParams(
            path=f"{self.host}{params.path}",
            options={
                **params.options,
                "headers": {
                    **params.options.get("headers", {}),
                    **auth_headers,
                },
            },
            bsh_options=params.bsh_options,
            api=params.api,
        )
        
        client_params = self._apply_pre_interceptors(client_params)
        response = self.http_client(client_params)
        return self._handle_response(response, client_params, "blob")

