# Third Party
# python std library
import random
from datetime import timedelta

# django
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# First Party
from user.models import User

# Local Folder
from .game_status import GameStatus
from .game_rules import GameRules
from .game_player_position import GamePlayerPosition


class Game(models.Model):
    """
    - Score in platform: points in game
    """

    class Meta:
        verbose_name_plural = _("Games")
        ordering = ["-game_datetime"]

    game_datetime = models.DateTimeField(
        verbose_name=_("Game date"), default=timezone.now, blank=True
    )
    status = models.SmallIntegerField(
        choices=GameStatus,
        default=GameStatus.SCHEDULED,
        verbose_name=_("Game status"),
    )
    duration = models.DurationField(default=timedelta(seconds=0), blank=True)

    rules = models.ForeignKey(
        to=GameRules, on_delete=models.RESTRICT, verbose_name=_("Game Rules")
    )

    _players = models.ManyToManyField(
        to=User, through="GamePlayer", related_name="games"
    )
    owner = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)

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
    def players(self):
        players = self.game_players.all().order_by("position")

        if not players.exists():
            return None, None

        if players.count() == 1:
            p = players[0]
            if p.position == GamePlayerPosition.LEFT:
                return p, None
            return None, p

        if players.count() == 2:
            return players[0], players[1]  # player_left, player_right

    @property
    def winner(self):
        if self.status != GameStatus.ENDED:
            return None

        players = self.game_players.order_by("-score")
        if not players.exists():
            return None
        return players.first()

    @property
    def is_a_tie(self) -> bool:
        if self.status != GameStatus.ENDED:
            return False

        player_left, player_right = self.players
        if player_left and player_right:
            if player_left.score == player_right.score:
                return True

        return False

    def add_player(self, user: User):
        self._players.add(user)

    def add_players(self, users: list[User]):
        self._players.add(*users)

    def set_players_position(self):
        players = self.game_players.all()
        if not players.exists() or players.count() != 2:
            return
        if players[0].position != players[1].position:
            return

        players_list = [p for p in players]
        random.shuffle(players_list)
        p1 = players_list[0]
        p2 = players_list[1]
        p1.position = GamePlayerPosition.LEFT
        p1.save()
        p2.position = GamePlayerPosition.RIGHT
        p2.save()
        return p1, p2

    def add_score(self) -> None:
        # tournament is other rule
        if hasattr(self, "round"):
            pass
        pass

    def get_player_name(self, player) -> str:
        """
        player is a GamePlayer instance
        """
        if player and player.user:
            return player.user.username
        return User.anonymous()["username"]

    def __str__(self) -> str:
        player_left, player_right = self.players
        p1 = self.get_player_name(player_left)
        p2 = self.get_player_name(player_right)

        return f"{p1} x {p2} - {str(self.game_datetime.date())}"

    def to_json(self) -> dict:
        player_left, player_right = self.players

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
            "player_left": player_left.to_json() if player_left else User.anonymous(),
            "player_right": player_right.to_json() if player_left else User.anonymous(),
            "owner": self.owner.resume_to_json() if self.owner else User.anonymous(),
        }
