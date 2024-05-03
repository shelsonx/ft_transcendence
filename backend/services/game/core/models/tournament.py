# python std library
from typing import Any

# django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Local Folder
from .game_rules import GameRules
from .game import Game
from .tournament_status import TournamentStatus

# First Party
from user.models import User


class TournamentType(models.IntegerChoices):
    CHALLENGE = 0, _("Challenge")  # e.g: best of 3
    ROUND_ROBIN = 1, _("Round-robin")  # pontos corridos
    ELIMINATION = 2, _("Elimination")  # mata-mata
    LEAGUE_WITH_PLAYOFF = 3, _("League with Playoff")  # misto


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

    # number_of_games
    number_of_games = models.PositiveSmallIntegerField(default=0)
    games = models.ManyToManyField(
        to=Game, related_name="tournament", verbose_name=_("Games")
    )

    # There must be a matchmaking system: the tournament system organize the
    # matchmaking of the participants, and announce the next fight
    def generate_games(self):
        self.__get_proxy().generate_games()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
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


# critério de desempate: a soma de pontos feitos
# se ainda assim tiver empate, uma última partida no formato do pong original

# tipos de campeonatos:


# 0) challenge
# - entre 2 jogadores
# - melhor de 3, 5 etc
class Challenge(Tournament):

    class Meta:
        proxy = True

    def generate_games(self):
        print("challenge")


# 1) pontos corridos
# - todos têm o mesmo número de jogos e todos enfrentam todos - deixar 2x padrão?
# - o vencedor ganha 3 pontos
# - empate cada um ganha 1 ponto
# - customizável: quantidade de jogos


class RoundRobin(Tournament):

    class Meta:
        proxy = True

    def generate_games(self):
        print("round-robin")


# 2) mata-mata
# quem ganhar segue pra próxima fase
# separado em fases
# precisa de um número par de equipes ?
# estrturar as chaves: Final, Semi-Final (4), quartas de final (8), oitavas de final 16


class Elimination(Tournament):

    class Meta:
        proxy = True

    def generate_games(self):
        print("elimination")


# 3) grupos + mata-mata
# - group size - aplica pontos corridos
# regra de classificação
# mata-mata


class LeaguePlayoff(Tournament):

    class Meta:
        proxy = True

    def generate_games(self):
        print("league with playoff")
