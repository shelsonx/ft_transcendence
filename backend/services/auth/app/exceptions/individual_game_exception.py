from .base_api_exception import BaseApiException
from django.utils.translation import gettext_lazy as _

class IndividualGameException(BaseApiException):

    def __init__(self):
        only_2_players = _("Only Two players are allowed to this mode of game")
        super().__init__(only_2_players, status_code=400)
