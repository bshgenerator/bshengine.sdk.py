"""Tests for BshClient class"""
import pytest
from unittest.mock import Mock, MagicMock
from bshengine import BshClient, BshError, BshResponse, AuthToken
from bshengine.client import BshClientFnParams


class TestBshClient:
    """Test BshClient class"""

    def test_constructor_with_host(self, mock_client_fn):
        """Test creating client with host"""
        client = BshClient(host="https://api.example.com", http_client=mock_client_fn)
        assert isinstance(client, BshClient)
        assert client.host == "https://api.example.com"

    def test_constructor_with_custom_client(self):
        """Test creating client with custom HTTP client"""
        custom_client = Mock()
        client = BshClient(host="", http_client=custom_client)
        assert isinstance(client, BshClient)

    def test_constructor_with_auth_fn(self, mock_client_fn):
        """Test creating client with auth function"""
        auth_fn = Mock(return_value=AuthToken(type="JWT", token="token"))
        client = BshClient(host="", http_client=mock_client_fn, auth_fn=auth_fn)
        assert isinstance(client, BshClient)

    def test_get_success(self, mock_client_fn):
        """Test successful GET request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            "data": [{"id": 1}],
            "code": 200,
            "status": "OK",
            "timestamp": 1234567890,
        }
        mock_response.content = b"test"
        
        def client_fn(params):
            return mock_response
        
        mock_request = client_fn
        mock_response.json.return_value = {
            "data": [{"id": 1}],
            "code": 200,
            "status": "OK",
            "timestamp": 1234567890,
        }
        
        client = BshClient(host="https://api.test.com", http_client=mock_request)
        
        params = BshClientFnParams(
            path="/users",
            options={},
            bsh_options={},
        )
        
        result = client.get(params)
        
        assert result is not None
        assert isinstance(result, BshResponse)
        assert result.code == 200

    def test_get_with_auth_headers(self, mock_client_fn):
        """Test GET request with authentication headers"""
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
        
        mock_request = Mock(return_value=mock_response)
        
        def auth_fn():
            return AuthToken(type="JWT", token="jwt-token-123")
        
        client = BshClient(
            host="https://api.test.com",
            http_client=mock_request,
            auth_fn=auth_fn,
        )
        
        params = BshClientFnParams(
            path="/test",
            options={},
            bsh_options={},
        )
        
        client.get(params)
        
        # Verify auth headers were added
        call_args = mock_request.call_args[0][0]
        assert "Authorization" in call_args.options.get("headers", {})
        assert call_args.options["headers"]["Authorization"] == "Bearer jwt-token-123"

    def test_get_with_api_key(self, mock_client_fn):
        """Test GET request with API key"""
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
        
        mock_request = Mock(return_value=mock_response)
        
        def auth_fn():
            return AuthToken(type="APIKEY", token="api-key-456")
        
        client = BshClient(
            host="https://api.test.com",
            http_client=mock_request,
            auth_fn=auth_fn,
        )
        
        params = BshClientFnParams(
            path="/test",
            options={},
            bsh_options={},
        )
        
        client.get(params)
        
        call_args = mock_request.call_args[0][0]
        assert "X-BSH-APIKEY" in call_args.options.get("headers", {})
        assert call_args.options["headers"]["X-BSH-APIKEY"] == "api-key-456"

    def test_get_error_response(self, mock_client_fn):
        """Test GET request with error response"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.ok = False
        mock_response.json.return_value = {
            "data": [],
            "code": 404,
            "status": "Not Found",
            "error": "Resource not found",
            "timestamp": 1234567890,
        }
        mock_response.content = b"test"
        
        mock_request = Mock(return_value=mock_response)
        mock_response.ok = False
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "data": [],
            "code": 404,
            "status": "Not Found",
            "error": "Resource not found",
            "timestamp": 1234567890,
        }
        
        client = BshClient(host="", http_client=mock_request)
        
        params = BshClientFnParams(
            path="/users",
            options={},
            bsh_options={},
        )
        
        with pytest.raises(BshError) as exc_info:
            client.get(params)
        
        assert exc_info.value.status == 404
        assert exc_info.value.endpoint == "/users"

    def test_get_with_on_error_callback(self, mock_client_fn):
        """Test GET request with on_error callback"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.ok = False
        mock_response.json.return_value = {
            "data": [],
            "code": 500,
            "status": "Error",
            "error": "Server error",
            "timestamp": 1234567890,
        }
        mock_response.content = b"test"
        
        mock_request = Mock(return_value=mock_response)
        mock_response.ok = False
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "data": [],
            "code": 500,
            "status": "Error",
            "error": "Server error",
            "timestamp": 1234567890,
        }
        
        client = BshClient(host="", http_client=mock_request)
        on_error = Mock()
        
        params = BshClientFnParams(
            path="/users",
            options={},
            bsh_options={"on_error": on_error},
        )
        
        result = client.get(params)
        
        assert result is None
        assert on_error.called

    def test_get_with_on_success_callback(self, mock_client_fn):
        """Test GET request with on_success callback"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            "data": [{"id": 1}],
            "code": 200,
            "status": "OK",
            "timestamp": 1234567890,
        }
        mock_response.content = b"test"
        
        mock_request = Mock(return_value=mock_response)
        mock_response.json.return_value = {
            "data": [{"id": 1}],
            "code": 200,
            "status": "OK",
            "timestamp": 1234567890,
        }
        
        client = BshClient(host="", http_client=mock_request)
        on_success = Mock()
        
        params = BshClientFnParams(
            path="/users",
            options={},
            bsh_options={"on_success": on_success},
        )
        
        result = client.get(params)
        
        assert result is None
        assert on_success.called

    def test_post_success(self, mock_client_fn):
        """Test successful POST request"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.ok = True
        mock_response.json.return_value = {
            "data": [{"id": 1}],
            "code": 201,
            "status": "Created",
            "timestamp": 1234567890,
        }
        mock_response.content = b"test"
        
        mock_request = Mock(return_value=mock_response)
        mock_response.json.return_value = {
            "data": [{"id": 1}],
            "code": 201,
            "status": "Created",
            "timestamp": 1234567890,
        }
        
        client = BshClient(host="https://api.test.com", http_client=mock_request)
        
        payload = {"name": "Test"}
        params = BshClientFnParams(
            path="/users",
            options={"body": payload},
            bsh_options={},
        )
        
        result = client.post(params)
        
        assert result is not None
        assert isinstance(result, BshResponse)
        assert result.code == 201

    def test_put_success(self, mock_client_fn):
        """Test successful PUT request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            "data": [{"id": 1}],
            "code": 200,
            "status": "OK",
            "timestamp": 1234567890,
        }
        mock_response.content = b"test"
        
        mock_request = Mock(return_value=mock_response)
        mock_response.json.return_value = {
            "data": [{"id": 1}],
            "code": 200,
            "status": "OK",
            "timestamp": 1234567890,
        }
        
        client = BshClient(host="https://api.test.com", http_client=mock_request)
        
        payload = {"name": "Updated"}
        params = BshClientFnParams(
            path="/users/1",
            options={"body": payload},
            bsh_options={},
        )
        
        result = client.put(params)
        
        assert result is not None
        assert isinstance(result, BshResponse)

    def test_delete_success(self, mock_client_fn):
        """Test successful DELETE request"""
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
        
        mock_request = Mock(return_value=mock_response)
        mock_response.json.return_value = {
            "data": [],
            "code": 200,
            "status": "OK",
            "timestamp": 1234567890,
        }
        
        client = BshClient(host="https://api.test.com", http_client=mock_request)
        
        params = BshClientFnParams(
            path="/users/1",
            options={},
            bsh_options={},
        )
        
        result = client.delete(params)
        
        assert result is not None
        assert isinstance(result, BshResponse)

    def test_patch_success(self, mock_client_fn):
        """Test successful PATCH request"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {
            "data": [{"id": 1}],
            "code": 200,
            "status": "OK",
            "timestamp": 1234567890,
        }
        mock_response.content = b"test"
        
        mock_request = Mock(return_value=mock_response)
        mock_response.json.return_value = {
            "data": [{"id": 1}],
            "code": 200,
            "status": "OK",
            "timestamp": 1234567890,
        }
        
        client = BshClient(host="https://api.test.com", http_client=mock_request)
        
        payload = {"name": "Patched"}
        params = BshClientFnParams(
            path="/users/1",
            options={"body": payload},
            bsh_options={},
        )
        
        result = client.patch(params)
        
        assert result is not None
        assert isinstance(result, BshResponse)

    def test_download_success(self, mock_client_fn):
        """Test successful download"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {}
        mock_response.content = b"test content"
        mock_response.text = "test"
        
        mock_request = Mock(return_value=mock_response)
        mock_response.content = b"test content"
        
        client = BshClient(host="https://api.test.com", http_client=mock_request)
        
        params = BshClientFnParams(
            path="/files/1",
            options={},
            bsh_options={},
        )
        
        result = client.download(params)
        
        assert result is not None
        assert isinstance(result, bytes)

    def test_download_with_callback(self, mock_client_fn):
        """Test download with on_download callback"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {}
        mock_response.content = b"test"
        mock_response.text = "test"
        
        mock_request = Mock(return_value=mock_response)
        mock_response.content = b"test"
        
        client = BshClient(host="", http_client=mock_request)
        on_download = Mock()
        
        params = BshClientFnParams(
            path="/files/1",
            options={},
            bsh_options={"on_download": on_download},
        )
        
        result = client.download(params)
        
        assert result is None
        assert on_download.called

    def test_no_auth_headers_for_auth_endpoints(self, mock_client_fn):
        """Test that auth headers are not added for auth endpoints"""
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
        
        mock_request = Mock(return_value=mock_response)
        
        def auth_fn():
            return AuthToken(type="JWT", token="token")
        
        client = BshClient(
            host="https://api.test.com",
            http_client=mock_request,
            auth_fn=auth_fn,
        )
        
        params = BshClientFnParams(
            path="/api/auth/login",
            options={},
            bsh_options={},
        )
        
        client.get(params)
        
        call_args = mock_request.call_args[0][0]
        headers = call_args.options.get("headers", {})
        assert "Authorization" not in headers

