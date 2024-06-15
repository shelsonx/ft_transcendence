from http import HTTPStatus

class BaseApiException(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self):
        return {"message": self.message, "status_code": self.status_code}


class UnauthorizedException(BaseApiException):

    def __init__(self, message="Unauthorized"):
        super().__init__(message=message, status_code=HTTPStatus.UNAUTHORIZED)
