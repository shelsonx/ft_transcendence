# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party
from user.models import User

# Local Folder
from .game_player_position import GamePlayerPosition


class GamePlayer(models.Model):
    game = models.ForeignKey(
        to="core.Game",
        on_delete=models.CASCADE,
        related_name="game_players",
        verbose_name=_("Game"),
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
    )
    score = models.IntegerField(default=0, verbose_name=_("Player' score in the game"))
    position = models.IntegerField(choices=GamePlayerPosition, default=0)

    class Meta:
        db_table = "game_player"
        unique_together = [["game", "user"]]

    @property
    def name(self):
        if self.user:
            t = self.game.get_tournament()
            if t:
                u = self.user
                tp = u.tournaments_player.filter(tournament=t, user=self.user).first()
                if tp:
                    return tp.name
            return self.user.username
        return User.anonymous()["username"]

    def to_json(self) -> dict:
        user = self.user
        return {
            "user": user.resume_to_json() if user else User.anonymous(),
            "score": self.score,
            "position": self.position,
        }

    def __str__(self) -> str:
        if self.user:
            return self.user.username
        return User.anonymous()["username"]
