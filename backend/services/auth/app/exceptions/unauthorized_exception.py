from .base_api_exception import BaseApiException

class UnauthorizedException(BaseApiException):
    
    def __init__(self, message = "Unauthorized"):
        super().__init__(message=message, status_code=401)
from .base_api_exception import BaseApiException


class UnauthorizedException(BaseApiException):

    def __init__(self, message="Unauthorized"):
        super().__init__(message=message, status_code=401)
