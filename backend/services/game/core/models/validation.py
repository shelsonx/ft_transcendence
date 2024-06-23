# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _

class VerificationType(models.TextChoices):
    GAME = "INDIVIDUAL_GAME", _("Game")
    TOURNAMENT = "TOURNAMENT", _("Accepted")
