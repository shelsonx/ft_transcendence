# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _


class GameStatus(models.IntegerChoices):
    PENDING = 0, _("Pending confirmation")
    SCHEDULED = 1, _("Scheduled")
    ONGOING = 2, _("Ongoing")
    PAUSED = 3, _("Paused")
    ENDED = 4, _("Ended")
    CANCELED = 5, _("Canceled")
