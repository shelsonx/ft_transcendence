# django
from django.db import models
from django.utils.translation import gettext_lazy as _


# Local Folder
from .game_rules import GameRules, GameRuleType
from .game_status import GameStatus
from .game import Game
from .round import Round
from .tournament_status import TournamentStatus
from .tournament_type import TournamentType

# First Party
from user.models import User


class Tournament(models.Model):
    """
        - Score in Tournament: winner wins 3 points, tie, 1 point
        - Score in platform: sum(score per game * points in game)
        - The winner wins a bonus of 10 points in platform score
    """

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
    def generate_rounds(self, *args, **kwargs) -> None:
        if self.status == TournamentStatus.ENDED:
            return

        if self.rounds.all().count():
            raise ValueError("Can't regenerate games if there are preexisting rounds")

        self.validate_number_of_players()
        self.__get_proxy().generate_rounds(*args, **kwargs)

    def generate_tiebreaker_game(self, player_a: User, player_b: User) -> Game:
        """
        The tiebraker game will be with the GameRuleType.PLAYER_POINTS default
        (wins who makes 11 points first)
        """

        round = Round.objects.create(
            round_number=(self.number_of_rounds + 1), number_of_games=1
        )
        game = Game.objects.create(
            status=GameStatus.SCHEDULED,
            rules=GameRules.objects.get(
                rule_type=GameRuleType.PLAYER_POINTS,
                points_to_win=11,
            ),
        )
        game.players.add(*[player_a, player_b])
        round.games.add(game)
        self.rounds.add(round)

        return game

    def validate_number_of_players(self) -> None:
        current_number_of_players = self.players.all().count()

        if current_number_of_players != self.number_of_players:
            raise ValueError(
                "mismatch between registered number of players and associated players"
            )

        self.__get_proxy().validate_number_of_players(current_number_of_players)

    def delete_rounds(self) -> None:
        if self.status == TournamentStatus.ENDED:
            raise ValueError("An Ended tournament can't have its rounds deleted")
        self.rounds.all().delete()

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
            # case TournamentType.LEAGUE_WITH_PLAYOFF:
            #     self._proxy = LeaguePlayoff.objects.get(pk=self.pk)

        return self._proxy

    def delete(self, using=None, keep_parents=False) -> tuple[int, dict[str, int]]:
        self.rounds.all().delete()
        return super().delete(using, keep_parents)


# critério de desempate: a soma de pontos feitos
# se ainda assim tiver empate, uma última partida no formato do pong original?

class Challenge(Tournament):
    """
        A Challenge Tournament is between 2 players only, in a style 'best of x',
        with x = the number of matches\n
        Each round has only one game between the players, i.e, the number of rounds
        and number of games are the same.\n
    """

    class Meta:
        proxy = True

    def generate_rounds(self, *args, **kwargs) -> None:
        for i in range(self.number_of_rounds):
            round = Round.objects.create(
                round_number=(i + 1), number_of_games=1
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


class RoundRobin(Tournament):
    """
        In a Round Robin Tournament:
        - all players play the same number of games
        - all players play against all other players at least one time (3 times maximum)
        - The number of rounds is (number_of_players - 1) * number of games against the
        same player
    """

    class Meta:
        proxy = True

    def generate_rounds(self, *args, **kwargs) -> None:
        print("round-robin")

    def validate_number_of_players(self, current_number_of_players: int) -> None:
        if current_number_of_players < 3:
            raise ValueError(
                "For Tournament Round Robin the number of players must be greater than"
                f"3, but {current_number_of_players} players were associated to it"
            )


class Elimination(Tournament):
    """
        In a Elimination Tournament:
        - who wins in each round pass to the next round
        - number_of_players must be even
        - maximum of 32 players?
        - The number of rounds is n for 2 ** n = number_of_players
    """

    class Meta:
        proxy = True

    def generate_rounds(self, *args, **kwargs) -> None:
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
# class LeaguePlayoff(Tournament):

#     class Meta:
#         proxy = True

#     def generate_rounds(self, *args, **kwargs):
#         print("league with playoff")
