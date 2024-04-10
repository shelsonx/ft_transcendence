# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party
from user.models import User

# Local Folder
from .match_status import MatchStatus


class Match(models.Model):

    class Meta:
        verbose_name_plural = _("matchs")

    datetime = models.DateTimeField(verbose_name=_("Match date"))
    status = models.CharField(
        max_length=1,
        choices=MatchStatus,
        default=MatchStatus.SCHEDULED,
        verbose_name=_("Match status"),
    )
    duration = models.DurationField()

    # Players data
    player_a = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Player A"),
        related_name=_("matchs_a"),
    )
    player_b = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Player B"),
        related_name=_("matchs_b"),
    )
    score_a = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("Player A Score")
    )
    score_b = models.PositiveSmallIntegerField(
        default=0, verbose_name=_("Player B Score")
    )

    # Rules
    # original pong
    # for each player to reach eleven points before the opponent;
    # if self.score_a == 11 or self.score_b == 11 -> ended
    player_reach_points = models.PositiveSmallIntegerField(default=11)  # min=5

    # different:
    # - sum of points == 11
    # if self.score_a + self.score_b == 11
    match_total_points = models.PositiveSmallIntegerField(
        default=None, null=True, blank=True
    )  # min=11
    max_duration = models.DurationField()

    @property
    def tournament(self):
        if hasattr(self, "tournament"):
            return self.tournament
        return None

    @property
    def winner(self) -> User | None:
        if self.status != MatchStatus.ENDED:
            return None
        if self.score_a > self.score_b:
            return self.player_a
        elif self.score_b > self.score_a:
            return self.player_b
        return None

    @property
    def is_a_tie(self) -> bool:
        if self.status == MatchStatus.ENDED:
            return self.score_a == self.score_b
        return False
