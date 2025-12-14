"""Main BSH Engine class"""
from typing import Optional, List, Callable, Any
from .client import BshClient, BshClientFn, BshAuthFn, BshRefreshTokenFn
from .types import AuthToken
from .client.types import BshPostInterceptor, BshPreInterceptor, BshErrorInterceptor
from .services import (
    EntityService,
    AuthService,
    UserService,
    SettingsService,
    ImageService,
    MailingService,
    BshUtilsService,
    CachingService,
    ApiKeyService,
)


class BshEngine:
    """Main BSH Engine SDK class"""

    def __init__(
        self,
        host: Optional[str] = None,
        api_key: Optional[str] = None,
        jwt_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        client_fn: Optional[BshClientFn] = None,
        auth_fn: Optional[BshAuthFn] = None,
        refresh_token_fn: Optional[BshRefreshTokenFn] = None,
        post_interceptors: Optional[List[BshPostInterceptor]] = None,
        pre_interceptors: Optional[List[BshPreInterceptor]] = None,
        error_interceptors: Optional[List[BshErrorInterceptor]] = None,
    ):
        self.host = host
        self._client_fn = client_fn
        self._auth_fn = auth_fn
        self._refresh_token_fn = refresh_token_fn
        self._post_interceptors: List[BshPostInterceptor] = post_interceptors or []
        self._pre_interceptors: List[BshPreInterceptor] = pre_interceptors or []
        self._error_interceptors: List[BshErrorInterceptor] = error_interceptors or []

        # Setup auth function if api_key or jwt_token provided
        if api_key and not auth_fn:
            self._auth_fn = lambda: AuthToken(type="APIKEY", token=api_key)
        elif jwt_token and not auth_fn:
            self._auth_fn = lambda: AuthToken(type="JWT", token=jwt_token)
        if refresh_token:
            self._refresh_token_fn = lambda: refresh_token

    def with_client(self, client_fn: BshClientFn) -> "BshEngine":
        """Set custom HTTP client function"""
        self._client_fn = client_fn
        return self

    def with_auth(self, auth_fn: BshAuthFn) -> "BshEngine":
        """Set authentication function"""
        self._auth_fn = auth_fn
        return self

    def with_refresh_token(self, refresh_token_fn: BshRefreshTokenFn) -> "BshEngine":
        """Set refresh token function"""
        self._refresh_token_fn = refresh_token_fn
        return self

    def post_interceptor(self, interceptor: BshPostInterceptor) -> "BshEngine":
        """Add post-request interceptor"""
        self._post_interceptors.append(interceptor)
        return self

    def pre_interceptor(self, interceptor: BshPreInterceptor) -> "BshEngine":
        """Add pre-request interceptor"""
        self._pre_interceptors.append(interceptor)
        return self

    def error_interceptor(self, interceptor: BshErrorInterceptor) -> "BshEngine":
        """Add error interceptor"""
        self._error_interceptors.append(interceptor)
        return self

    def get_post_interceptors(self) -> List[BshPostInterceptor]:
        """Get post interceptors"""
        return self._post_interceptors

    def get_pre_interceptors(self) -> List[BshPreInterceptor]:
        """Get pre interceptors"""
        return self._pre_interceptors

    def get_error_interceptors(self) -> List[BshErrorInterceptor]:
        """Get error interceptors"""
        return self._error_interceptors

    @property
    def _client(self) -> BshClient:
        """Get BSH client instance"""
        return BshClient(
            host=self.host,
            http_client=self._client_fn,
            auth_fn=self._auth_fn,
            refresh_token_fn=self._refresh_token_fn,
            bsh_engine=self,
        )

    @property
    def entities(self) -> EntityService:
        """Get entities service"""
        return EntityService(self._client)

    def entity(self, entity: str) -> EntityService:
        """Get entity service for specific entity"""
        return EntityService(self._client, entity)

    @property
    def core(self) -> dict:
        """Get core entities"""
        from .types import (
            BshEntities,
            BshSchemas,
            BshTypes,
            BshUser,
            BshPolicy,
            BshRole,
            BshFiles,
            BshConfigurations,
            SentEmail,
            BshEmailTemplate,
            BshEventLogs,
            BshTrigger,
            BshTriggerInstance,
        )
        return {
            "BshEntities": self.entity("BshEntities"),
            "BshSchemas": self.entity("BshSchemas"),
            "BshTypes": self.entity("BshTypes"),
            "BshUsers": self.entity("BshUsers"),
            "BshPolicies": self.entity("BshPolicies"),
            "BshRoles": self.entity("BshRoles"),
            "BshFiles": self.entity("BshFiles"),
            "BshConfigurations": self.entity("BshConfigurations"),
            "BshEmails": self.entity("BshEmails"),
            "BshEmailTemplates": self.entity("BshEmailTemplates"),
            "BshEventLogs": self.entity("BshEventLogs"),
            "BshTriggers": self.entity("BshTriggers"),
            "BshTriggerInstances": self.entity("BshTriggerInstances"),
        }

    @property
    def auth(self) -> AuthService:
        """Get auth service"""
        return AuthService(self._client)

    @property
    def user(self) -> UserService:
        """Get user service"""
        return UserService(self._client)

    @property
    def settings(self) -> SettingsService:
        """Get settings service"""
        return SettingsService(self._client)

    @property
    def image(self) -> ImageService:
        """Get image service"""
        return ImageService(self._client)

    @property
    def mailing(self) -> MailingService:
        """Get mailing service"""
        return MailingService(self._client)

    @property
    def utils(self) -> BshUtilsService:
        """Get utils service"""
        return BshUtilsService(self._client)

    @property
    def caching(self) -> CachingService:
        """Get caching service"""
        return CachingService(self._client)

    @property
    def api_key(self) -> ApiKeyService:
        """Get API key service"""
        return ApiKeyService(self._client)

