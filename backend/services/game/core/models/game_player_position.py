from django.db import models
from django.utils.translation import gettext_lazy as _


class GamePlayerPosition(models.IntegerChoices):
    LEFT = "0", _("Left")
    RIGHT = "1", _("Right")
