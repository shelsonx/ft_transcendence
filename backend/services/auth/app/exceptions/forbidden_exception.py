from .base_api_exception import BaseApiException


class ForbiddenException(BaseApiException):

    def __init__(self, message: str = "Forbidden"):
        super().__init__(message=message, status_code=403)
