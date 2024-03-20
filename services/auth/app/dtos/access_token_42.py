from typing import Any
from dataclasses import dataclass
import json

@dataclass
class AccessToken42:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str
    created_at: int
    secret_valid_until: int

    @staticmethod
    def from_dict(obj: Any) -> 'AccessToken42':
        _access_token = str(obj.get("access_token"))
        _token_type = str(obj.get("token_type"))
        _expires_in = int(obj.get("expires_in"))
        _refresh_token = str(obj.get("refresh_token"))
        _scope = str(obj.get("scope"))
        _created_at = int(obj.get("created_at"))
        _secret_valid_until = int(obj.get("secret_valid_until"))
        return AccessToken42(_access_token, _token_type, _expires_in, _refresh_token, _scope, _created_at, _secret_valid_until)
