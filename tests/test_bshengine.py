"""Tests for BshEngine class"""
from unittest.mock import Mock, MagicMock
import pytest
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

    @pytest.fixture
    def mock_client_fn(self):
        """Mock client function for tests"""
        def client_fn(params):
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.ok = True
            mock_response.json.return_value = {
                "data": [],
                "code": 200,
                "status": "OK",
                "timestamp": 1234567890,
            }
            mock_response.content = b"test"
            mock_response.text = "test"
            return mock_response
        return client_fn

    def test_constructor_requires_host_and_client_fn(self):
        """Test that host and client_fn are required"""
        with pytest.raises(TypeError):
            BshEngine()

    def test_constructor_default(self, mock_client_fn):
        """Test creating engine with default values"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        assert isinstance(engine, BshEngine)
        assert engine.get_post_interceptors() == []
        assert engine.get_pre_interceptors() == []
        assert engine.get_error_interceptors() == []

    def test_constructor_with_host(self, mock_client_fn):
        """Test creating engine with host"""
        engine = BshEngine("https://api.example.com", mock_client_fn)
        assert isinstance(engine, BshEngine)
        assert engine.host == "https://api.example.com"

    def test_constructor_with_api_key(self, mock_client_fn):
        """Test creating engine with API key"""
        engine = BshEngine("https://api.test.com", mock_client_fn, api_key="test-api-key")
        assert isinstance(engine, BshEngine)
        # Verify auth function is set by checking it returns correct token
        auth_fn = engine._auth_fn
        assert auth_fn is not None
        auth_token = auth_fn()
        assert auth_token.type == "APIKEY"
        assert auth_token.token == "test-api-key"

    def test_constructor_with_jwt_token(self, mock_client_fn):
        """Test creating engine with JWT token"""
        engine = BshEngine("https://api.test.com", mock_client_fn, jwt_token="test-jwt-token")
        assert isinstance(engine, BshEngine)
        # Verify auth function is set by checking it returns correct token
        auth_fn = engine._auth_fn
        assert auth_fn is not None
        auth_token = auth_fn()
        assert auth_token.type == "JWT"
        assert auth_token.token == "test-jwt-token"

    def test_constructor_with_refresh_token(self, mock_client_fn):
        """Test creating engine with refresh token"""
        engine = BshEngine("https://api.test.com", mock_client_fn, refresh_token="test-refresh-token")
        assert isinstance(engine, BshEngine)
        refresh_token_fn = engine._refresh_token_fn
        assert refresh_token_fn is not None
        assert refresh_token_fn() == "test-refresh-token"

    def test_constructor_with_custom_client_fn(self):
        """Test creating engine with custom client function"""
        custom_client_fn = Mock()
        engine = BshEngine("https://api.test.com", custom_client_fn)
        assert isinstance(engine, BshEngine)
        assert engine._client_fn == custom_client_fn

    def test_constructor_with_custom_auth_fn(self, mock_client_fn):
        """Test creating engine with custom auth function"""
        custom_auth_fn = Mock(return_value=AuthToken(type="JWT", token="token"))
        engine = BshEngine("https://api.test.com", mock_client_fn, auth_fn=custom_auth_fn)
        assert isinstance(engine, BshEngine)
        assert engine._auth_fn == custom_auth_fn

    def test_constructor_with_interceptors(self, mock_client_fn):
        """Test creating engine with interceptors"""
        post_interceptor = Mock()
        pre_interceptor = Mock()
        error_interceptor = Mock()
        
        engine = BshEngine(
            "https://api.test.com",
            mock_client_fn,
            post_interceptors=[post_interceptor],
            pre_interceptors=[pre_interceptor],
            error_interceptors=[error_interceptor],
        )
        
        assert isinstance(engine, BshEngine)
        assert len(engine.get_post_interceptors()) == 1
        assert len(engine.get_pre_interceptors()) == 1
        assert len(engine.get_error_interceptors()) == 1

    def test_with_client(self, mock_client_fn):
        """Test with_client method"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        custom_client_fn = Mock()
        result = engine.with_client(custom_client_fn)
        
        assert result is engine
        assert engine._client_fn == custom_client_fn

    def test_with_auth(self, mock_client_fn):
        """Test with_auth method"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        custom_auth_fn = Mock()
        result = engine.with_auth(custom_auth_fn)
        
        assert result is engine
        assert engine._auth_fn == custom_auth_fn

    def test_with_refresh_token(self, mock_client_fn):
        """Test with_refresh_token method"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        custom_refresh_fn = Mock()
        result = engine.with_refresh_token(custom_refresh_fn)
        
        assert result is engine
        assert engine._refresh_token_fn == custom_refresh_fn

    def test_entities_property(self, mock_client_fn):
        """Test entities property"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        entities = engine.entities
        assert isinstance(entities, EntityService)

    def test_entity_method(self, mock_client_fn):
        """Test entity method"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        entity_service = engine.entity("CustomEntity")
        assert isinstance(entity_service, EntityService)

    def test_core_property(self, mock_client_fn):
        """Test core property"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        core = engine.core
        assert isinstance(core, dict)
        assert "BshEntities" in core
        assert "BshSchemas" in core
        assert "BshTypes" in core
        assert "BshUsers" in core
        assert all(isinstance(v, EntityService) for v in core.values())

    def test_auth_property(self, mock_client_fn):
        """Test auth property"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        auth = engine.auth
        assert isinstance(auth, AuthService)

    def test_user_property(self, mock_client_fn):
        """Test user property"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        user = engine.user
        assert isinstance(user, UserService)

    def test_settings_property(self, mock_client_fn):
        """Test settings property"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        settings = engine.settings
        assert isinstance(settings, SettingsService)

    def test_image_property(self, mock_client_fn):
        """Test image property"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        image = engine.image
        assert isinstance(image, ImageService)

    def test_mailing_property(self, mock_client_fn):
        """Test mailing property"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        mailing = engine.mailing
        assert isinstance(mailing, MailingService)

    def test_utils_property(self, mock_client_fn):
        """Test utils property"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        utils = engine.utils
        assert isinstance(utils, BshUtilsService)

    def test_caching_property(self, mock_client_fn):
        """Test caching property"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        caching = engine.caching
        assert isinstance(caching, CachingService)

    def test_api_key_property(self, mock_client_fn):
        """Test api_key property"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        api_key = engine.api_key
        assert isinstance(api_key, ApiKeyService)

    def test_post_interceptor(self, mock_client_fn):
        """Test post_interceptor method"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        interceptor = Mock()
        result = engine.post_interceptor(interceptor)
        
        assert result is engine
        assert len(engine.get_post_interceptors()) == 1
        assert engine.get_post_interceptors()[0] == interceptor

    def test_pre_interceptor(self, mock_client_fn):
        """Test pre_interceptor method"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        interceptor = Mock()
        result = engine.pre_interceptor(interceptor)
        
        assert result is engine
        assert len(engine.get_pre_interceptors()) == 1
        assert engine.get_pre_interceptors()[0] == interceptor

    def test_error_interceptor(self, mock_client_fn):
        """Test error_interceptor method"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        interceptor = Mock()
        result = engine.error_interceptor(interceptor)
        
        assert result is engine
        assert len(engine.get_error_interceptors()) == 1
        assert engine.get_error_interceptors()[0] == interceptor

    def test_multiple_interceptors(self, mock_client_fn):
        """Test adding multiple interceptors"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
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

    def test_method_chaining(self, mock_client_fn):
        """Test method chaining"""
        engine = BshEngine("https://api.test.com", mock_client_fn)
        result = engine.with_client(Mock()).with_auth(Mock())
        
        assert result is engine

    def test_jwt_priority_over_api_key(self, mock_client_fn):
        """Test that JWT token takes priority over API key"""
        engine = BshEngine("https://api.test.com", mock_client_fn, api_key="api-key", jwt_token="jwt-token")
        auth_fn = engine._auth_fn
        assert auth_fn is not None
        auth_token = auth_fn()
        assert auth_token.type == "JWT"
        assert auth_token.token == "jwt-token"

