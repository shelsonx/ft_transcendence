from .base_api_exception import BaseApiException
from django.utils.translation import gettext_lazy as _

invalid_msg = _("Invalid Access Token")
class InvalidAccessToken(BaseApiException):

    def __init__(self, message=invalid_msg):
        super().__init__(message=message, status_code=401)
