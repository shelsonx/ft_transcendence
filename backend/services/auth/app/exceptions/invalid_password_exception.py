from .base_api_exception import BaseApiException
from django.utils.translation import gettext_lazy as _


class InvalidPasswordException(BaseApiException):

    def __init__(self):
        bad_crendentials = _("bad credentials")
        super().__init__(message=bad_crendentials, status_code=401)
