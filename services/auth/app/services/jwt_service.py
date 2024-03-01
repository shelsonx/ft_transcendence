
from ..interfaces.services.token_service import ITokenService
from ..models.user import User
from datetime import datetime, timedelta
import base64
import json
import hmac
import os
from ..constants.env_variables import EnvVariables
from ..exceptions.unauthorized_exception import Unauthorized
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
      raise Unauthorized()
    split_token = token.split('.')
    if len(split_token) != 3:
      raise Unauthorized()
    base64header, base64payload, signature = split_token
    generated_signature = self._generate_signature(base64header, base64payload)
    if generated_signature != signature:
      raise Unauthorized()
    payload = json.loads(base64.b64decode(base64payload).decode("utf-8"))
    return JWTPayload.decode(payload)