# Third Party
from django.db import models
from django.utils.translation import gettext_lazy as _


from .game import Game
from .status import GameStatus, RoundStatus
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

    def get_next_or_current_game(self) -> Game | None:
        not_completed_games = None

        match self.status:
            case RoundStatus.ENDED:
                return None
            case RoundStatus.WAITING:
                not_completed_games = self.games.filter(status=GameStatus.TOURNAMENT)
            case RoundStatus.ON_GOING:
                status = [GameStatus.SCHEDULED, GameStatus.ONGOING, GameStatus.PAUSED]
                not_completed_games = self.games.filter(status__in=status)
                if not not_completed_games.exists():
                    status = GameStatus.TOURNAMENT
                    not_completed_games = self.games.filter(status=status)
            case _:
                raise NotImplementedError()

        if not_completed_games is None:
            return None
        return not_completed_games.order_by("game_datetime").first()

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
