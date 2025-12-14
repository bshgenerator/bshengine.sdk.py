"""Tests for BshEngine class"""
import pytest
from unittest.mock import Mock, MagicMock
from bshengine import BshEngine, AuthToken
from bshengine.services import (
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


class TestBshEngine:
    """Test BshEngine class"""

    def test_constructor_default(self):
        """Test creating engine with default values"""
        engine = BshEngine()
        assert isinstance(engine, BshEngine)
        assert engine.get_post_interceptors() == []
        assert engine.get_pre_interceptors() == []
        assert engine.get_error_interceptors() == []

    def test_constructor_with_host(self):
        """Test creating engine with host"""
        engine = BshEngine(host="https://api.example.com")
        assert isinstance(engine, BshEngine)
        assert engine.host == "https://api.example.com"

    def test_constructor_with_api_key(self):
        """Test creating engine with API key"""
        engine = BshEngine(api_key="test-api-key")
        assert isinstance(engine, BshEngine)
        # Verify auth function is set by checking it returns correct token
        auth_fn = engine._auth_fn
        assert auth_fn is not None
        auth_token = auth_fn()
        assert auth_token.type == "APIKEY"
        assert auth_token.token == "test-api-key"

    def test_constructor_with_jwt_token(self):
        """Test creating engine with JWT token"""
        engine = BshEngine(jwt_token="test-jwt-token")
        assert isinstance(engine, BshEngine)
        # Verify auth function is set by checking it returns correct token
        auth_fn = engine._auth_fn
        assert auth_fn is not None
        auth_token = auth_fn()
        assert auth_token.type == "JWT"
        assert auth_token.token == "test-jwt-token"

    def test_constructor_with_refresh_token(self):
        """Test creating engine with refresh token"""
        engine = BshEngine(refresh_token="test-refresh-token")
        assert isinstance(engine, BshEngine)
        refresh_token_fn = engine._refresh_token_fn
        assert refresh_token_fn is not None
        assert refresh_token_fn() == "test-refresh-token"

    def test_constructor_with_custom_client_fn(self):
        """Test creating engine with custom client function"""
        custom_client_fn = Mock()
        engine = BshEngine(client_fn=custom_client_fn)
        assert isinstance(engine, BshEngine)
        assert engine._client_fn == custom_client_fn

    def test_constructor_with_custom_auth_fn(self):
        """Test creating engine with custom auth function"""
        custom_auth_fn = Mock(return_value=AuthToken(type="JWT", token="token"))
        engine = BshEngine(auth_fn=custom_auth_fn)
        assert isinstance(engine, BshEngine)
        assert engine._auth_fn == custom_auth_fn

    def test_constructor_with_interceptors(self):
        """Test creating engine with interceptors"""
        post_interceptor = Mock()
        pre_interceptor = Mock()
        error_interceptor = Mock()
        
        engine = BshEngine(
            post_interceptors=[post_interceptor],
            pre_interceptors=[pre_interceptor],
            error_interceptors=[error_interceptor],
        )
        
        assert isinstance(engine, BshEngine)
        assert len(engine.get_post_interceptors()) == 1
        assert len(engine.get_pre_interceptors()) == 1
        assert len(engine.get_error_interceptors()) == 1

    def test_with_client(self):
        """Test with_client method"""
        engine = BshEngine()
        custom_client_fn = Mock()
        result = engine.with_client(custom_client_fn)
        
        assert result is engine
        assert engine._client_fn == custom_client_fn

    def test_with_auth(self):
        """Test with_auth method"""
        engine = BshEngine()
        custom_auth_fn = Mock()
        result = engine.with_auth(custom_auth_fn)
        
        assert result is engine
        assert engine._auth_fn == custom_auth_fn

    def test_with_refresh_token(self):
        """Test with_refresh_token method"""
        engine = BshEngine()
        custom_refresh_fn = Mock()
        result = engine.with_refresh_token(custom_refresh_fn)
        
        assert result is engine
        assert engine._refresh_token_fn == custom_refresh_fn

    def test_entities_property(self):
        """Test entities property"""
        engine = BshEngine()
        entities = engine.entities
        assert isinstance(entities, EntityService)

    def test_entity_method(self):
        """Test entity method"""
        engine = BshEngine()
        entity_service = engine.entity("CustomEntity")
        assert isinstance(entity_service, EntityService)

    def test_core_property(self):
        """Test core property"""
        engine = BshEngine()
        core = engine.core
        assert isinstance(core, dict)
        assert "BshEntities" in core
        assert "BshSchemas" in core
        assert "BshTypes" in core
        assert "BshUsers" in core
        assert all(isinstance(v, EntityService) for v in core.values())

    def test_auth_property(self):
        """Test auth property"""
        engine = BshEngine()
        auth = engine.auth
        assert isinstance(auth, AuthService)

    def test_user_property(self):
        """Test user property"""
        engine = BshEngine()
        user = engine.user
        assert isinstance(user, UserService)

    def test_settings_property(self):
        """Test settings property"""
        engine = BshEngine()
        settings = engine.settings
        assert isinstance(settings, SettingsService)

    def test_image_property(self):
        """Test image property"""
        engine = BshEngine()
        image = engine.image
        assert isinstance(image, ImageService)

    def test_mailing_property(self):
        """Test mailing property"""
        engine = BshEngine()
        mailing = engine.mailing
        assert isinstance(mailing, MailingService)

    def test_utils_property(self):
        """Test utils property"""
        engine = BshEngine()
        utils = engine.utils
        assert isinstance(utils, BshUtilsService)

    def test_caching_property(self):
        """Test caching property"""
        engine = BshEngine()
        caching = engine.caching
        assert isinstance(caching, CachingService)

    def test_api_key_property(self):
        """Test api_key property"""
        engine = BshEngine()
        api_key = engine.api_key
        assert isinstance(api_key, ApiKeyService)

    def test_post_interceptor(self):
        """Test post_interceptor method"""
        engine = BshEngine()
        interceptor = Mock()
        result = engine.post_interceptor(interceptor)
        
        assert result is engine
        assert len(engine.get_post_interceptors()) == 1
        assert engine.get_post_interceptors()[0] == interceptor

    def test_pre_interceptor(self):
        """Test pre_interceptor method"""
        engine = BshEngine()
        interceptor = Mock()
        result = engine.pre_interceptor(interceptor)
        
        assert result is engine
        assert len(engine.get_pre_interceptors()) == 1
        assert engine.get_pre_interceptors()[0] == interceptor

    def test_error_interceptor(self):
        """Test error_interceptor method"""
        engine = BshEngine()
        interceptor = Mock()
        result = engine.error_interceptor(interceptor)
        
        assert result is engine
        assert len(engine.get_error_interceptors()) == 1
        assert engine.get_error_interceptors()[0] == interceptor

    def test_multiple_interceptors(self):
        """Test adding multiple interceptors"""
        engine = BshEngine()
        post1 = Mock()
        post2 = Mock()
        pre1 = Mock()
        error1 = Mock()
        
        engine.post_interceptor(post1).post_interceptor(post2)
        engine.pre_interceptor(pre1)
        engine.error_interceptor(error1)
        
        assert len(engine.get_post_interceptors()) == 2
        assert len(engine.get_pre_interceptors()) == 1
        assert len(engine.get_error_interceptors()) == 1

    def test_method_chaining(self):
        """Test method chaining"""
        engine = BshEngine()
        result = engine.with_client(Mock()).with_auth(Mock())
        
        assert result is engine

    def test_jwt_priority_over_api_key(self):
        """Test that JWT token takes priority over API key"""
        engine = BshEngine(api_key="api-key", jwt_token="jwt-token")
        auth_fn = engine._auth_fn
        assert auth_fn is not None
        auth_token = auth_fn()
        assert auth_token.type == "JWT"
        assert auth_token.token == "jwt-token"

