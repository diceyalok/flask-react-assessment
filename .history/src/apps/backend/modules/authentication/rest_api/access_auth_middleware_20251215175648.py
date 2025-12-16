from functools import wraps
from typing import Any, Callable

from flask import request

from modules.authentication.authentication_service import AuthenticationService
from modules.authentication.errors import (
    AuthorizationHeaderNotFoundError,
    InvalidAuthorizationHeaderError,
    UnauthorizedAccessError,
)


