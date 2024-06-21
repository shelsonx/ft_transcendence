# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _

class VerificationType(models.IntegerChoices):
    GAME = 0, _("Game")
    TOURNAMENT = 1, _("Accepted")
