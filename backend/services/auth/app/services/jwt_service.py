
from ..interfaces.services.token_service import ITokenService
from ..models.user import User
from datetime import datetime, timedelta
import base64
import json
import hmac
import os
from ..constants.env_variables import EnvVariables
from ..exceptions.unauthorized_exception import UnauthorizedException
from ..entities.jwt_payload import JWTPayload
from ..utils.uuid_encoder import UUIDEncoder

class JWTService(ITokenService):

  def _generate_signature(self, base64_encoded_header: str, base64_encoded_payload: str) -> str:
    message = f"{base64_encoded_header}.{base64_encoded_payload}"
    secret = os.getenv(EnvVariables.JWT_SECRET)
    signature = hmac.new(secret.encode(), message.encode(), digestmod='SHA256').digest()
    base64_url_signature = base64.urlsafe_b64encode(signature).rstrip(b'=')
    return base64_url_signature.decode()

  def create_token(self, user: User) -> str:
    header = {
      "alg": "HS256",
      "typ": "JWT",
    }
    payload = JWTPayload.create(user.id, 2).to_dict()
    base64_header = base64.b64encode(json.dumps(header).encode("utf-8")).decode("utf-8")
    base64_payload = base64.b64encode(json.dumps(payload, cls=UUIDEncoder).encode("utf-8")).decode("utf-8")
    signature = self._generate_signature(base64_header, base64_payload)
    return f"{base64_header}.{base64_payload}.{signature}"
  
  def verify_token(self, token: str) -> JWTPayload:
    if token is None:
      raise UnauthorizedException()
    split_token = token.split('.')
    if len(split_token) != 3:
      raise UnauthorizedException()
    base64header, base64payload, signature = split_token
    generated_signature = self._generate_signature(base64header, base64payload)
    if generated_signature != signature:
      raise UnauthorizedException()
    payload = json.loads(base64.b64decode(base64payload).decode("utf-8"))
    return JWTPayload.decode(payload)
from ..interfaces.services.token_service import ITokenService
from ..models.user import User
from datetime import datetime, timedelta
import base64
import json
import hmac
import os
from ..constants.env_variables import EnvVariables
from ..exceptions.unauthorized_exception import UnauthorizedException
from ..entities.jwt_payload import JWTPayload
from ..utils.uuid_encoder import UUIDEncoder


class JWTService(ITokenService):

    def __init__(self) -> None:
        self.secret = os.getenv(EnvVariables.JWT_SECRET)

    def _get_secret(self, secret: str) -> str:
        if secret is None or secret == "":
            return self.secret
        return secret

    def _generate_signature(
        self,
        base64_encoded_header: str,
        base64_encoded_payload: str,
        secret: str = None,
    ) -> str:
        secret = self._get_secret(secret)
        message = f"{base64_encoded_header}.{base64_encoded_payload}"
        signature = hmac.new(
            secret.encode(), message.encode(), digestmod="SHA256"
        ).digest()
        base64_url_signature = base64.urlsafe_b64encode(signature).rstrip(b"=")
        return base64_url_signature.decode()

    def create_token(
        self, user: User, expires_in_hours: int, secret: str = None
    ) -> str:
        header = {
            "alg": "HS256",
            "typ": "JWT",
        }
        payload = JWTPayload.create(user.id, expires_in_hours).to_dict()
        base64_header = base64.b64encode(json.dumps(header).encode("utf-8")).decode(
            "utf-8"
        )
        base64_payload = base64.b64encode(
            json.dumps(payload, cls=UUIDEncoder).encode("utf-8")
        ).decode("utf-8")
        signature = self._generate_signature(base64_header, base64_payload, secret)
        return f"{base64_header}.{base64_payload}.{signature}"

    def verify_token(self, token: str, secret: str = None) -> JWTPayload:
        if token is None:
            raise UnauthorizedException()
        split_token = token.split(".")
        if len(split_token) != 3:
            raise UnauthorizedException()
        base64header, base64payload, signature = split_token
        payload = json.loads(base64.b64decode(base64payload).decode("utf-8"))
        decoded_payload = JWTPayload.decode(payload)
        if decoded_payload.is_expired():
            raise UnauthorizedException(message="Token expired")
        generated_signature = self._generate_signature(
            base64header, base64payload, secret
        )
        if generated_signature != signature:
            raise UnauthorizedException()
        return decoded_payload

    def get_token_expiration(self, token: str, secret: str = None) -> datetime:
        payload = self.verify_token(token, secret)
        return payload.exp
