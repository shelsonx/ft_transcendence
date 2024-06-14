# django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local Folder
from .tournament import Tournament

# First Party
from user.models import User


#  at the start of a tournament, each player must input their alias name. The aliases
# will be reset when a new tournament begins
# Users can select a unique display name to play the tournaments
class TournamentPlayer(models.Model):
    tournament = models.ForeignKey(
        to=Tournament,
        on_delete=models.CASCADE,
        related_name="tournament_players",
        verbose_name=_("Tournament"),
    )
    user = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, related_name="tournaments_player", null=True
    )
    alias_name = models.CharField(
        max_length=20, verbose_name=_("Alias name"), blank=True
    )
    score = models.IntegerField(
        default=0, verbose_name=_("Score")
    )
    rating = models.IntegerField(
        default=0, verbose_name=_("Rating")
    )

    class Meta:
        db_table = "tournament_player"
        unique_together = [["tournament", "user"]]

    def __str__(self) -> str:
        if self.alias_name:
            return self.alias_name
        if self.user:
            return self.user.username
        return User.anonymous()["username"]
