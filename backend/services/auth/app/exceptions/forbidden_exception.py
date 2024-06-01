from .base_api_exception import BaseApiException
from django.utils.translation import gettext_lazy as _

forbidden = _("Forbidden")
class ForbiddenException(BaseApiException):
    def __init__(self, message: str = forbidden):
        super().__init__(message=message, status_code=403)
