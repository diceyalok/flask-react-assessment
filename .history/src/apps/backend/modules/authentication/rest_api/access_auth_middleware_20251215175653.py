from functools import wraps
from typing import Any, Callable

from flask import request

from modules.authentication.authentication_service import AuthenticationService
from modules.authentication.errors import (
    AuthorizationHeaderNotFoundError,
    InvalidAuthorizationHeaderError,
    UnauthorizedAccessError,
)


def access_auth_middleware(next_func: Callable) -> Callable:
    @wraps(next_func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"--- DEBUG MIDDLEWARE START ---")
        
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            print("ERROR: Authorization header missing")
            raise AuthorizationHeaderNotFoundError("Authorization header is missing.")

        print(f"Header found: {auth_header[:15]}...") # Print start of token

        try:
            auth_scheme, auth_token = auth_header.split(" ")
        except ValueError:
             print("ERROR: Header format invalid (Not 'Bearer <token>')")
             raise InvalidAuthorizationHeaderError("Invalid authorization header.")

        if auth_scheme != "Bearer" or not auth_token:
            print("ERROR: Scheme is not Bearer")
            raise InvalidAuthorizationHeaderError("Invalid authorization header.")

        # Verify the token
        try:
            auth_payload = AuthenticationService.verify_access_token(token=auth_token)
            print(f"Token Valid! User ID in Token: {auth_payload.account_id}")
        except Exception as e:
            print(f"ERROR: Token Verification Failed: {e}")
            raise e

        # Check against URL parameters
        if "account_id" in kwargs:
            url_account_id = kwargs["account_id"]
            print(f"URL Requesting Account ID: {url_account_id}")
            
            if str(auth_payload.account_id) != str(url_account_id):
                print(f"ERROR: ID MISMATCH! Token {auth_payload.account_id} != URL {url_account_id}")
                raise UnauthorizedAccessError("Unauthorized access.")
            else:
                print("SUCCESS: IDs Match.")
        else:
            print("WARNING: No 'account_id' in URL kwargs to check.")

        setattr(request, "account_id", auth_payload.account_id)
        print("--- DEBUG MIDDLEWARE END ---")
        return next_func(*args, **kwargs)

    return wrapper