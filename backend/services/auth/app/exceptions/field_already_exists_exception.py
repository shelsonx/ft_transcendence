from .base_api_exception import BaseApiException
from django.utils.translation import gettext_lazy as _


class FieldAlreadyExistsException(BaseApiException):
    def __init__(self, field: str):
        msg = _("field already exists")
        print(msg)
        super().__init__(message=f"{field} {msg}", status_code=400)
