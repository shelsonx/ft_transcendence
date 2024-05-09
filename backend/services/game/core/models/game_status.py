# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _


class GameStatus(models.IntegerChoices):
    PENDING = 0, _("Pending confirmation")
    SCHEDULED = 1, _("Scheduled")
    ONGOING = 2, _("Ongoing")
    ENDED = 3, _("Ended")
    CANCELED = 4, _("Canceled")
