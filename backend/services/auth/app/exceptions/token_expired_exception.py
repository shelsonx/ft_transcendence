from .base_api_exception import BaseApiException
from django.utils.translation import gettext_lazy as _

token_expired = _("Token Expired")
class TokenExpiredException(BaseApiException):

    def __init__(self, message=token_expired):
        super().__init__(message=message, status_code=401)
