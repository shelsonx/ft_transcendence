# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _

from .game import Game
from .tournament_type import TournamentType

class Round(models.Model):
    number_of_games = models.PositiveSmallIntegerField(default=0)
    games = models.ManyToManyField(
        to=Game, related_name="round", verbose_name=_("Games"),
    )
    round_number = models.IntegerField(default=1)

    @property
    def number_of_players(self) -> int:
        tournament = self.tournament

        match tournament.tournament_type:
            case TournamentType.CHALLENGE:
                return 2
            case TournamentType.ROUND_ROBIN:
                return tournament.number_of_players
            case TournamentType.ELIMINATION:
                return tournament.number_of_players >> self.round_number - 1

    def label(self):
        if self.tournament.tournament_type == TournamentType.ELIMINATION:
            match int(self.number_of_players):
                case 8:
                    return _("quarter-finals")
                case 4:
                    return _("semi-final")
                case 2:
                    return _("final")
                case _:
                    return _(f"{id} round")

        return _(f"{id} round")

    def __str__(self):
        return self.label()

    def delete(self, using=None, keep_parents=False) -> tuple[int, dict[str, int]]:
        self.games.all().delete()
        return super().delete(using, keep_parents)
