# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _

# First Party
from user.models import User


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

    class Meta:
        db_table = "game_player"
