"""Tests for AuthService"""
import pytest
from unittest.mock import Mock, MagicMock
from bshengine.services import AuthService
from bshengine import BshClient, BshResponse


class TestAuthService:
    """Test AuthService class"""

    @pytest.fixture
    def mock_client(self):
        """Create mock client"""
        client = Mock(spec=BshClient)
        client.post = Mock()
        return client

    @pytest.fixture
    def auth_service(self, mock_client):
        """Create AuthService instance"""
        return AuthService(mock_client)

    def test_login(self, auth_service, mock_client):
        """Test login method"""
        mock_response = BshResponse(
            data=[{"access": "access-token", "refresh": "refresh-token"}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.post.return_value = mock_response

        payload = {"email": "test@example.com", "password": "password123"}
        result = auth_service.login(payload)

        assert mock_client.post.called
        call_args = mock_client.post.call_args[0][0]
        assert call_args.path == "/api/auth/login"
        assert call_args.options["body"] == payload
        assert call_args.api == "auth.login"
        assert result == mock_response

    def test_register(self, auth_service, mock_client):
        """Test register method"""
        mock_response = BshResponse(
            data=[{"userId": "1", "email": "test@example.com"}],
            code=201,
            status="Created",
            timestamp=1234567890,
        )
        mock_client.post.return_value = mock_response

        payload = {
            "email": "test@example.com",
            "password": "password123",
            "profile": {"firstName": "Test", "lastName": "User"},
        }
        result = auth_service.register(payload)

        assert mock_client.post.called
        call_args = mock_client.post.call_args[0][0]
        assert call_args.path == "/api/auth/register"
        assert call_args.options["body"] == payload
        assert call_args.api == "auth.register"
        assert result == mock_response

    def test_refresh_token(self, auth_service, mock_client):
        """Test refresh_token method"""
        mock_response = BshResponse(
            data=[{"access": "new-access-token", "refresh": "new-refresh-token"}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.post.return_value = mock_response

        payload = {"refresh": "old-refresh-token"}
        result = auth_service.refresh_token(payload)

        assert mock_client.post.called
        call_args = mock_client.post.call_args[0][0]
        assert call_args.path == "/api/auth/refresh"
        assert call_args.options["body"] == payload
        assert call_args.api == "auth.refreshToken"
        assert result == mock_response

    def test_forget_password(self, auth_service, mock_client):
        """Test forget_password method"""
        mock_response = BshResponse(
            data=[{}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.post.return_value = mock_response

        payload = {"email": "test@example.com"}
        result = auth_service.forget_password(payload)

        assert mock_client.post.called
        call_args = mock_client.post.call_args[0][0]
        assert call_args.path == "/api/auth/forget-password"
        assert call_args.options["body"] == payload
        assert call_args.api == "auth.forgetPassword"
        assert result == mock_response

    def test_reset_password(self, auth_service, mock_client):
        """Test reset_password method"""
        mock_response = BshResponse(
            data=[{}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.post.return_value = mock_response

        payload = {
            "email": "test@example.com",
            "code": "123456",
            "newPassword": "newpassword123",
        }
        result = auth_service.reset_password(payload)

        assert mock_client.post.called
        call_args = mock_client.post.call_args[0][0]
        assert call_args.path == "/api/auth/reset-password"
        assert call_args.options["body"] == payload
        assert call_args.api == "auth.resetPassword"
        assert result == mock_response

    def test_activate_account(self, auth_service, mock_client):
        """Test activate_account method"""
        mock_response = BshResponse(
            data=[{}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.post.return_value = mock_response

        payload = {"email": "test@example.com", "code": "123456"}
        result = auth_service.activate_account(payload)

        assert mock_client.post.called
        call_args = mock_client.post.call_args[0][0]
        assert call_args.path == "/api/auth/activate-account"
        assert call_args.options["body"] == payload
        assert call_args.api == "auth.activateAccount"
        assert result == mock_response

    def test_login_with_callbacks(self, auth_service, mock_client):
        """Test login with callbacks"""
        mock_response = BshResponse(
            data=[{"access": "token", "refresh": "refresh"}],
            code=200,
            status="OK",
            timestamp=1234567890,
        )
        mock_client.post.return_value = mock_response

        on_success = Mock()
        on_error = Mock()

        auth_service.login(
            payload={"email": "test@example.com", "password": "pass"},
            on_success=on_success,
            on_error=on_error,
        )

        assert mock_client.post.called
        call_args = mock_client.post.call_args[0][0]
        assert call_args.bsh_options["on_success"] == on_success
        assert call_args.bsh_options["on_error"] == on_error

