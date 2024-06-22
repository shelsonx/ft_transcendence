# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _


class GameStatus(models.IntegerChoices):
    PENDING = 0, _("Pending confirmation")
    TOURNAMENT = 1, _("Scheduled")
    SCHEDULED = 2, _("Scheduled")
    ONGOING = 3, _("Ongoing")
    PAUSED = 4, _("Paused")
    ENDED = 5, _("Ended")
    CANCELED = 6, _("Canceled")


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
