# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _

class TournamentStatus(models.IntegerChoices):
    INVITATION = 0, _("Waiting all players confirmation")
    SCHEDULED = 1, _("Scheduled")  # all players already confirmed
    ON_GOING = 2, _("On going")
    ENDED = 3, _("Ended")
    CANCELED = 4, _("Canceled")
