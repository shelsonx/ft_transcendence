from .base_api_exception import BaseApiException
from django.utils.translation import gettext_lazy as _

class UserNotFoundException(BaseApiException):

    def __init__(self):
        user_not_found = _("User not found")
        super().__init__(user_not_found, status_code=404)
