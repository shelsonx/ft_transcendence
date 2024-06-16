# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _


from .game import Game
from .status import RoundStatus
from .tournament_type import TournamentType


class Round(models.Model):
    tournament = models.ForeignKey(
        to="core.Tournament", on_delete=models.CASCADE, related_name="rounds"
    )
    number_of_games = models.PositiveSmallIntegerField(default=0)
    games = models.ManyToManyField(
        to=Game,
        related_name="round",
        verbose_name=_("Games"),
    )
    round_number = models.IntegerField(default=1)
    status = models.IntegerField(
        choices=RoundStatus.choices,
        default=RoundStatus.WAITING,
        verbose_name=_("Tournament Status"),
    )

    @property
    def number_of_players(self) -> int:
        t = self.tournament

        match t.tournament_type:
            case TournamentType.CHALLENGE:
                return 2
            case TournamentType.ROUND_ROBIN:
                return t.number_of_players
            # case TournamentType.ELIMINATION:
            #     return tournament.number_of_players >> self.round_number - 1

    def label(self):
        # t = self.tournament
        # if t.tournament_type == TournamentType.ELIMINATION:
        #     match int(self.number_of_players):
        #         case 8:
        #             return _("quarter-finals")
        #         case 4:
        #             return _("semi-final")
        #         case 2:
        #             return _("final")
        #         case _:
        #             return _(f"{id} round")

        return str(_(f"Round {self.round_number}"))

    def delete(self, using=None, keep_parents=False) -> tuple[int, dict[str, int]]:
        self.games.all().delete()
        return super().delete(using, keep_parents)
