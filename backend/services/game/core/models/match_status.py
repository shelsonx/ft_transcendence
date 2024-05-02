# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _

class MatchStatus(models.IntegerChoices):
    SCHEDULED = 0, _("Scheduled")
    WAITING = 1, _("Waiting players confirmation to beggin")
    ONGOING = 2, _("Ongoing")
    ENDED = 3, _("Ended")
