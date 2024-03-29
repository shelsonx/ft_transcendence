from .base_api_exception import BaseApiException


class UserInactiveException(BaseApiException):

    def __init__(self):
        super().__init__(
            "User is inactive, you must confirm the code by e-mail", status_code=400
        )
