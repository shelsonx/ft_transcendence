from .base_api_exception import BaseApiException


class TokenExpiredException(BaseApiException):

    def __init__(self, message="Token Expired"):
        super().__init__(message=message, status_code=401)
