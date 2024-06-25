# Python std library
import base64
import hmac
import os

# First party
from user_management_api.exception.exception import UnauthorizedException
from .model import JWTPayload

class JWTService:

    def __init__(self) -> None:
        self.secret = os.getenv("JWT_SECRET")

    def verify_token(self, token: str, secret: str = None) -> JWTPayload:
        if token is None:
            raise UnauthorizedException()

        split_token = token.split(".")
        if len(split_token) != 3:
            raise UnauthorizedException()

        base64header, base64payload, signature = split_token
        decoded_payload = JWTPayload.decode(base64payload)
        if decoded_payload.is_expired():
            raise UnauthorizedException(message="Token expired")

        generated_signature = self.__generate_signature(
            base64header, base64payload, secret
        )
        if generated_signature != signature:
            raise UnauthorizedException()
        return decoded_payload

    def __get_secret(self, secret: str) -> str:
        if secret is None or secret == "":
            return self.secret
        return secret

    def __generate_signature(
        self,
        base64_encoded_header: str,
        base64_encoded_payload: str,
        secret: str = None,
    ) -> str:
        secret = self.__get_secret(secret)
        message = f"{base64_encoded_header}.{base64_encoded_payload}"
        signature = hmac.new(
            secret.encode(), message.encode(), digestmod="SHA256"
        ).digest()
        base64_url_signature = base64.urlsafe_b64encode(signature).rstrip(b"=")
        return base64_url_signature.decode()
