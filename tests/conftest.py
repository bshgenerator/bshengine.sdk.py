"""Pytest configuration and fixtures"""
import pytest
from unittest.mock import Mock, MagicMock
from bshengine import BshEngine, BshClient, AuthToken


@pytest.fixture
def mock_requests(monkeypatch):
    """Mock requests library"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.ok = True
    mock_response.json.return_value = {
        "data": [],
        "code": 200,
        "status": "OK",
        "timestamp": 1234567890,
    }
    mock_response.content = b"test content"
    mock_response.text = "test"
    
    mock_request = Mock(return_value=mock_response)
    monkeypatch.setattr("bshengine.client.bsh_client.requests.request", mock_request)
    
    return mock_request, mock_response


@pytest.fixture
def mock_client_fn():
    """Mock client function"""
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
        return mock_response
    return client_fn


@pytest.fixture
def mock_auth_fn():
    """Mock auth function"""
    def auth_fn():
        return AuthToken(type="JWT", token="test-token")
    return auth_fn


@pytest.fixture
def engine():
    """Create BshEngine instance"""
    return BshEngine(host="https://api.test.com")


@pytest.fixture
def client(mock_client_fn, mock_auth_fn):
    """Create BshClient instance"""
    return BshClient(
        host="https://api.test.com",
        http_client=mock_client_fn,
        auth_fn=mock_auth_fn,
    )

