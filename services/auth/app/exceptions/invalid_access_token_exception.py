from .base_api_exception import BaseApiException


class InvalidAccessToken(BaseApiException):

    def __init__(self, message="Invalid Access Token"):
        super().__init__(message=message, status_code=401)
