"""Authentication types"""
from typing import Optional, Literal
from dataclasses import dataclass


@dataclass
class AuthToken:
    """Authentication token"""
    type: str  # "JWT" or "APIKEY"
    token: str
    
    @classmethod
    def from_dict(cls, data: dict) -> "AuthToken":
        """Create AuthToken from dict"""
        return cls(type=data.get("type", "JWT"), token=data.get("token", ""))


@dataclass
class LoginParams:
    """Login parameters"""
    email: str
    password: str


@dataclass
class AuthTokens:
    """Authentication tokens response"""
    access: str
    refresh: str

