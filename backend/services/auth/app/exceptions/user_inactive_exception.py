from .base_api_exception import BaseApiException
from django.utils.translation import gettext_lazy as _

class UserInactiveException(BaseApiException):

    def __init__(self):
        user_inactive = _("User is inactive, you must confirm the code by e-mail")
        super().__init__(
            user_inactive, status_code=400
        )
