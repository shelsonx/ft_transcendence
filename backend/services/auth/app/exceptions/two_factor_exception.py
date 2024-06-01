from .base_api_exception import BaseApiException
from django.utils.translation import gettext_lazy as _

two_factor_required = _("Two factor code required")
class TwoFactorCodeException(BaseApiException):

    def __init__(self, message: str = two_factor_required):
        super().__init__(message=message, status_code=400)
