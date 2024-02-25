from .BaseApiException import BaseApiException

class InvalidPasswordException(BaseApiException):
    
    def __init__(self):
        super().__init__(message="Bad Credentials", status_code=401)