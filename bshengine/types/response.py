"""Response types and error handling"""
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass, field


@dataclass
class BshResponse:
    """Response structure from BSH Engine API"""
    data: List[Any]
    timestamp: int
    code: int
    status: str
    error: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    pagination: Optional[Dict[str, Any]] = None
    endpoint: Optional[str] = None
    api: Optional[str] = None
    validations: Optional[List[Dict[str, str]]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BshResponse":
        """Create BshResponse from dictionary"""
        return cls(
            data=data.get("data", []),
            timestamp=data.get("timestamp", 0),
            code=data.get("code", 0),
            status=data.get("status", ""),
            error=data.get("error"),
            meta=data.get("meta"),
            pagination=data.get("pagination"),
            endpoint=data.get("endpoint"),
            api=data.get("api"),
            validations=data.get("validations"),
        )


def is_ok(response: Optional[BshResponse]) -> bool:
    """Check if response is successful"""
    if response is None:
        return False
    return 200 <= response.code < 300


class BshError(Exception):
    """Error raised by BSH Engine API"""

    def __init__(
        self,
        status: int,
        endpoint: str,
        response: Optional[BshResponse] = None,
    ):
        self.status = status
        self.endpoint = endpoint
        self.response = response
        if response:
            response.endpoint = endpoint
        message = str(response) if response else f"HTTP {status} error at {endpoint}"
        super().__init__(message)
        self.name = "BshError"

