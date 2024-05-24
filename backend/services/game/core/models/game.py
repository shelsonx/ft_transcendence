# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party
from user.models import User

# Local Folder
from .game_status import GameStatus
from .game_rules import GameRules


class Game(models.Model):
    """
    - Score in platform: points in game
    """

    class Meta:
        verbose_name_plural = _("Games")
        ordering = ["-game_datetime"]

    game_datetime = models.DateTimeField(verbose_name=_("Game date"), null=True)  # remove null
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

    # field to link Elimination Tournament Games
    # result_to = models.ForeignKey(
    #     "self",
    #     on_delete=models.SET_NULL,
    #     related_name="depends_on",
    #     null=True,
    #     blank=True,
    # )

    # @property
    # def tournament(self):
    #     if hasattr(self, "tournament"):
    #         return self.tournament
    #     return None

    @property
    def winner(self) -> User | None:
        if self.status != GameStatus.ENDED:
            return None

        players = self.game_players.order_by("-score")
        if not players.exists():
            return None
        return players.first().user

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

    def add_score(self) -> None:
        # tournament is other rule
        if hasattr(self, "round"):
            pass
        pass

    def __str__(self) -> str:
        # players =
        # name = " x ".join([])
        return str(self.game_datetime.date())

    def to_json(self) -> dict:
        players = self.game_players.all()
        player_left = players.first()
        player_right = players.last()

        seconds = self.duration.seconds
        minutes = seconds // 60
        seconds = seconds % 60

        return {
            "id": self.pk,
            "game_datetime": self.game_datetime,
            "status": self.status,
            "duration": {
                "minutes": minutes,
                "seconds": seconds,
            },
            "rules": self.rules.to_json(),
            "player_left": player_left.to_json(),
            "player_right": player_right.to_json(),
        }
