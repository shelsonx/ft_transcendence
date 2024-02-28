from .BaseApiException import BaseApiException

class Unauthorized(BaseApiException):
    
    def __init__(self, message = "Unauthorized"):
        super().__init__(message=message, status_code=401)