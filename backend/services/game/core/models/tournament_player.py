# django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local Folder
from .tournament import Tournament
from .status import PlayerStatus

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
    winnings = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    ties = models.PositiveIntegerField(default=0)
    _updated_players = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    class Meta:
        db_table = "tournament_player"
        unique_together = [["tournament", "user"]]

    @property
    def name(self) -> str:
        if self.alias_name:
            return self.alias_name
        if self.user:
            return self.user.username
        return User.anonymous()["username"]

    @property
    def status(self) -> str:
        if self.verified:
            return PlayerStatus.ACCEPTED.label
        return PlayerStatus.PENDING.label

    def update_user(self, *, force: bool = False):
        if self._updated_players and not force:
            return

        user = self.user
        if not user:
            return

        user.score += self.score
        user.rating += self.rating
        user.winnings += self.winnings
        user.losses += self.losses
        user.ties += self.ties
        user.save()
        self._updated_players = True
        self.save()

    def __str__(self) -> str:
        description = ""
        an = self.alias_name if self.alias_name else ""
        user = self.user.username if self.user else ""
        if an and user:
            description = f"{user} as {an}"
        elif an:
            description = an
        elif user:
            description = user
        else:
            description = User.anonymous()["username"]
        return description
