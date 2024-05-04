# django
from django.db import models
from django.utils.translation import gettext_lazy as _


# Local Folder
from .game_rules import GameRules
from .game_status import GameStatus
from .game import Game
from .round import Round
from .tournament_status import TournamentStatus
from .tournament_type import TournamentType

# First Party
from user.models import User


class Tournament(models.Model):
    tournament_type = models.SmallIntegerField(
        choices=TournamentType.choices,
        default=TournamentType.CHALLENGE,
        verbose_name=_("Tournament Type"),
    )
    status = models.IntegerField(
        choices=TournamentStatus.choices,
        default=TournamentStatus.INVITATION,
        verbose_name=_("Tournament Status"),
    )

    # All players and games must adhere to the same game rules
    rules = models.ForeignKey(
        to=GameRules,
        on_delete=models.RESTRICT,
        verbose_name=_("Tournament Rules"),
    )

    number_of_players = models.PositiveSmallIntegerField(default=2)
    players = models.ManyToManyField(
        to=User,
        through="core.TournamentPlayer",
        related_name="tournaments",
        verbose_name=_("Tournament Players"),
    )

    # total games in CHALLENGE (is the same as total games for each player) - inputed
    # total games for each player against each other in ROUND_ROBIN - inputed
    # total games in ELIMINATION (it is calculated based on number_of_players)
    # number_of_games = models.PositiveSmallIntegerField(default=0)
    number_of_rounds = models.PositiveSmallIntegerField(default=1)
    rounds = models.ManyToManyField(
        to=Round, related_name="tournament", verbose_name=_("Rounds")
    )

    # There must be a matchmaking system: the tournament system organize the
    # matchmaking of the participants, and announce the next fight
    def generate_games(self, *args, **kwargs) -> None:
        self.validate_number_of_players()
        self.__get_proxy().generate_games(*args, **kwargs)

    def validate_number_of_players(self) -> None:
        current_number_of_players = self.players.all().count()

        if current_number_of_players != self.number_of_players:
            raise ValueError(
                "mismatch between registered number of players and associated players"
            )

        self.__get_proxy().validate_number_of_players(current_number_of_players)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._proxy = None

    def __get_proxy(self):
        if self._proxy and self._proxy.tournament_type == self.tournament_type:
            return self._proxy

        if not self.pk:
            raise ValueError("You need to save the object")

        match self.tournament_type:
            case TournamentType.CHALLENGE:
                self._proxy = Challenge.objects.get(pk=self.pk)
            case TournamentType.ROUND_ROBIN:
                self._proxy = RoundRobin.objects.get(pk=self.pk)
            case TournamentType.ELIMINATION:
                self._proxy = Elimination.objects.get(pk=self.pk)
            case TournamentType.LEAGUE_WITH_PLAYOFF:
                self._proxy = LeaguePlayoff.objects.get(pk=self.pk)

        return self._proxy

    def delete(self, using=None, keep_parents=False) -> tuple[int, dict[str, int]]:
        self.rounds.all().delete()
        return super().delete(using, keep_parents)


# critério de desempate: a soma de pontos feitos
# se ainda assim tiver empate, uma última partida no formato do pong original

# tipos de campeonatos:


# 0) challenge
# - entre 2 jogadores
# - melhor de 3, 5 etc
class Challenge(Tournament):

    class Meta:
        proxy = True

    def generate_games(self, *args, **kwargs) -> None:
        rounds = self.rounds.all()
        total_existing_rounds = rounds.count()
        if total_existing_rounds == self.number_of_rounds:
            return

        if total_existing_rounds > self.number_of_rounds:
            raise ValueError("mismatch between actual rounds and registered rounds")

        # since for Challenge Tournament a winner may win before all rounds happen
        # we just generate a round at time
        round = Round.objects.create(
            round_number=(total_existing_rounds + 1),
            number_of_games=1
        )
        game = Game.objects.create(
            status=GameStatus.SCHEDULED,
            rules=self.rules,
        )
        game.players.add(*self.players.all())
        round.games.add(game)
        self.rounds.add(round)

    def validate_number_of_players(self, current_number_of_players: int) -> None:
        if current_number_of_players != 2:
            raise ValueError(
                "For Tournament Challenge the number of players must be 2, "
                f"but {current_number_of_players} players were associated to it"
            )

# 1) pontos corridos
# - todos têm o mesmo número de jogos e todos enfrentam todos - deixar 2x padrão?
# - o vencedor ganha 3 pontos
# - empate cada um ganha 1 ponto
# - customizável: quantidade de jogos


class RoundRobin(Tournament):

    class Meta:
        proxy = True

    def generate_games(self, *args, **kwargs) -> None:
        print("round-robin")

    def validate_number_of_players(self, current_number_of_players: int) -> None:
        if current_number_of_players < 3:
            raise ValueError(
                "For Tournament Round Robin the number of players must be greater than"
                f"3, but {current_number_of_players} players were associated to it"
            )


# 2) mata-mata
# quem ganhar segue pra próxima fase
# separado em fases
# precisa de um número par de equipes ?
# estrturar as chaves: Final, Semi-Final (4), quartas de final (8), oitavas de final 16


class Elimination(Tournament):

    class Meta:
        proxy = True

    def generate_games(self, *args, **kwargs) -> None:
        print("elimination")

    def validate_number_of_players(self, current_number_of_players: int):
        if current_number_of_players < 4:
            raise ValueError(
                "For Tournament Round Robin the number of players must be greater than"
                f"3, but {current_number_of_players} players were associated to it"
            )

        if current_number_of_players % 2:
            raise ValueError(
                "For Tournament Round Robin the number of players must be even"
            )


# 3) grupos + mata-mata
# - group size - aplica pontos corridos
# regra de classificação
# mata-mata


class LeaguePlayoff(Tournament):

    class Meta:
        proxy = True

    def generate_games(self, *args, **kwargs):
        print("league with playoff")
