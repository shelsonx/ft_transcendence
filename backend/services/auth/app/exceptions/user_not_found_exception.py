
from .base_api_exception import BaseApiException

class UserNotFoundException(BaseApiException):
    
    def __init__(self):
        super().__init__("User not found", status_code = 404)