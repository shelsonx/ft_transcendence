from .base_api_exception import BaseApiException


class ForbiddenException(BaseApiException):

    def __init__(self):
        super().__init__(message="Forbidden", status_code=403)
