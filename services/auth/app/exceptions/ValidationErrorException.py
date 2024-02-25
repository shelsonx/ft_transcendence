
from .BaseApiException import BaseApiException

class ValidationErrorException(BaseApiException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)