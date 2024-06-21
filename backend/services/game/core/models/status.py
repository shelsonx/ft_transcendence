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


class TournamentStatus(models.IntegerChoices):
    INVITATION = 0, _("Waiting all players confirmation")
    SCHEDULED = 1, _("Scheduled")  # all players already confirmed
    ON_GOING = 2, _("On going")
    ENDED = 3, _("Ended")
    CANCELED = 4, _("Canceled")


class RoundStatus(models.IntegerChoices):
    WAITING = 0, _("Didn't started")
    ON_GOING = 1, _("On going")
    ENDED = 2, _("Ended")

class PlayerStatus(models.IntegerChoices):
    PENDING = 0, _("Pending")
    ACCEPTED = 1, _("Accepted")
