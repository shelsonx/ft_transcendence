from .base_api_exception import BaseApiException
from typing import List, Union


class NotValidPasswordException(BaseApiException):
    def __init__(self, message: Union[str, List[str]]):
        super().__init__(message=message, status_code=400)
