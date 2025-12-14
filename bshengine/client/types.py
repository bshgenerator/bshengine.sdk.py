"""Client type definitions"""
from typing import Callable, Optional, Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .bsh_client import BshClientFnParams

from ..types import BshResponse, BshError

# Type aliases for callbacks
BshClientFn = Callable[["BshClientFnParams"], Any]  # Returns requests.Response-like object
BshAuthFn = Callable[[], Any]  # Returns AuthToken or None
BshRefreshTokenFn = Callable[[], Any]  # Returns str or None
BshPostInterceptor = Callable[[BshResponse, Optional["BshClientFnParams"]], Any]  # Returns BshResponse
BshPreInterceptor = Callable[["BshClientFnParams"], Any]  # Returns BshClientFnParams
BshErrorInterceptor = Callable[[BshError, Optional[BshResponse], Optional["BshClientFnParams"]], Any]  # Returns BshError or None

