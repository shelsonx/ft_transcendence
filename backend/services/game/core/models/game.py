# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party
from user.models import User

# Local Folder
from .game_status import GameStatus
from .game_rules import GameRules


class Game(models.Model):

    class Meta:
        verbose_name_plural = _("Games")
        ordering = ["game_datetime"]

    game_datetime = models.DateTimeField(verbose_name=_("Game date"))
    status = models.SmallIntegerField(
        choices=GameStatus,
        default=GameStatus.SCHEDULED,
        verbose_name=_("Game status"),
    )
    duration = models.DurationField(null=True)

    rules = models.ForeignKey(
        to=GameRules, on_delete=models.RESTRICT, verbose_name=_("Game Rules")
    )

    players = models.ManyToManyField(
        to=User, through="GamePlayer", related_name="games"
    )

    # @property
    # def tournament(self):
    #     if hasattr(self, "tournament"):
    #         return self.tournament
    #     return None

    @property
    def winner(self) -> User | None:
        if self.status != GameStatus.ENDED:
            return None
        raise NotImplementedError("property not implemented")

    #     if self.score_a > self.score_b:
    #         return self.player_a
    #     elif self.score_b > self.score_a:
    #         return self.player_b
    #     return None

    @property
    def is_a_tie(self) -> bool:
        raise NotImplementedError("property not implemented")

    #     if self.status == GameStatus.ENDED:
    #         return self.score_a == self.score_b
    #     return False


# class Pong(Game):
#     pass
