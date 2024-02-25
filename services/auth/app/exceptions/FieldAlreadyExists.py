from .BaseApiException import BaseApiException

class FieldAlreadyExists(BaseApiException):
    def __init__(self, field: str):
        super().__init__(message=f"{field} already exists", status_code=400)