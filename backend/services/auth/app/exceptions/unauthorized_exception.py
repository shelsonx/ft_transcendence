from .base_api_exception import BaseApiException
from django.utils.translation import gettext_lazy as _

unauthorized = _("Unauthorized")
class UnauthorizedException(BaseApiException):

    def __init__(self, message=unauthorized):
        super().__init__(message=message, status_code=401)
