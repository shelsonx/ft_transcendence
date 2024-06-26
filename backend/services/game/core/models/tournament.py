# python std library
from pprint import pprint
import random
import math
from typing import Any

# django
from django.db import models
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _


# Local Folder
from .game_rules import GameRules, GameRuleType
from .status import GameStatus, RoundStatus, TournamentStatus
from .game import Game
from .round import Round
from .tournament_type import TournamentType

# First Party
from user.models import User


class Tournament(models.Model):
    """
    - Score in Tournament: winner wins 3 points, tie, 1 point
    - Score in platform: sum(score per game * points in game)
    - The winner wins a bonus of 10 points in platform score
    """

    name = models.CharField(max_length=50, verbose_name=_("Name"))
    tournament_type = models.SmallIntegerField(
        choices=TournamentType.choices,
        default=TournamentType.CHALLENGE,
        verbose_name=_("Type"),
    )
    status = models.IntegerField(
        choices=TournamentStatus.choices,
        default=TournamentStatus.INVITATION,
        verbose_name=_("Status"),
    )
    tournament_date = models.DateTimeField(verbose_name=_("Date"))

    # All players and games must adhere to the same game rules
    rules = models.ForeignKey(
        to=GameRules,
        on_delete=models.RESTRICT,
        verbose_name=_("Rules"),
    )

    number_of_players = models.PositiveSmallIntegerField(
        default=2, verbose_name=_("Number of players")
    )
    _players = models.ManyToManyField(
        to=User,
        through="core.TournamentPlayer",
        related_name="tournaments",
        verbose_name=_("Players"),
    )
    _updated_players = models.BooleanField(default=False)
    owner = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True, verbose_name=_("Creator")
    )

    # value inputed for CHALLENGE (is the same as total games for each player)
    # value calculated for ROUND_ROBIN based on number_of_players
    # value calculated for ELIMINATION based on number_of_players
    number_of_rounds = models.PositiveSmallIntegerField(
        default=2, verbose_name=_("Number of rounds")
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._proxy = None
        self.__players = None
        self._winner = None

    @property
    def players(self) -> QuerySet:
        if self.__players:
            return self.__players

        self.__players = (
            self.tournament_players.all()
            .select_related("user")
            .order_by("-score", "-winnings", "-rating")
        )
        return self.__players

    @property
    def winner(self):
        if self.status != TournamentStatus.ENDED:
            return None

        if self._winner:
            return self._winner

        self._winner = self.players.first()
        return self._winner

    def add_player(self, user: User):
        self._players.add(user)

    def add_players(self, users: list[User]):
        self._players.add(*users)

    def get_rounds(self) -> QuerySet:
        return self.rounds.all().order_by("round_number")

    def get_next_or_current_round(self) -> Round | None:
        if self.status in [
            TournamentStatus.INVITATION,
            TournamentStatus.ENDED,
            TournamentStatus.CANCELED,
        ]:
            return None

        rounds = self.get_rounds().exclude(status=RoundStatus.ENDED)
        return rounds.first()

    def get_next_or_current_game(self) -> Game | None:
        if self.status in [
            TournamentStatus.INVITATION,
            TournamentStatus.ENDED,
            TournamentStatus.CANCELED,
        ]:
            return None

        r = self.get_next_or_current_round()
        if r:
            return r.get_next_or_current_game()

        return None

    def update_users(self, *, force: bool = False) -> None:
        if self.status != TournamentStatus.ENDED:
            return
        if self._updated_players and not force:
            return

        for p in self.players:
            p.update_user(force=force)

    # There must be a matchmaking system: the tournament system organize the
    # matchmaking of the participants, and announce the next fight
    def generate_rounds(self, *args, **kwargs) -> None:
        if self.status != TournamentStatus.SCHEDULED:
            return

        rounds = self.rounds.all()
        if rounds.count():
            raise ValueError("Can't regenerate games if there are preexisting rounds")

        self.validate_number_of_players()
        self.__get_proxy().generate_rounds(*args, **kwargs)

    def generate_game(self) -> Game:
        return Game.objects.create(
            status=GameStatus.TOURNAMENT,
            rules=self.rules,
            owner=self.owner,
        )

    def generate_round(self, round_nbr: int, nbr_of_games: int) -> Round:
        return Round.objects.create(
            tournament=self,
            round_number=round_nbr,
            number_of_games=nbr_of_games,
            status=RoundStatus.WAITING,
        )

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
        game.add_players([player_a, player_b])
        game.set_players_position()
        round.games.add(game)
        self.rounds.add(round)

        return game

    def validate_number_of_players(self) -> None:
        current_number_of_players = self.players.count()

        if current_number_of_players != self.number_of_players:
            raise ValueError(
                "mismatch between registered number of players and associated players"
            )

        self.__get_proxy().validate_number_of_players(current_number_of_players)

    def delete_rounds(self) -> None:
        if self.status == TournamentStatus.ENDED:
            raise ValueError("An Ended tournament can't have its rounds deleted")
        self.rounds.all().delete()

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
            # case TournamentType.ELIMINATION:
            #     self._proxy = Elimination.objects.get(pk=self.pk)
            # case TournamentType.LEAGUE_WITH_PLAYOFF:
            #     self._proxy = LeaguePlayoff.objects.get(pk=self.pk)

        return self._proxy

    def save(self, *args, **kwargs) -> None:
        if self.number_of_players:
            match self.tournament_type:
                case TournamentType.ROUND_ROBIN:
                    self.number_of_rounds = (
                        self.number_of_players - 1 + self.number_of_players % 2
                    )
                # case TournamentType.ELIMINATION:
                #     self.number_of_rounds = math.ceil(math.log2(self.number_of_players))

        if not self.name:
            self.__set_name()

        return super().save(*args, **kwargs)

    def __set_name(self):
        if self.tournament_type == TournamentType.CHALLENGE:
            self.name = f"Best of {self.number_of_rounds}"
        else:
            nb = Tournament.objects.count()
            self.name = f"Tournament {nb + 1}"

    def __str__(self):
        return self.name


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
        users = [u for u in self._players.all()]
        for i in range(self.number_of_rounds):
            round = self.generate_round(i + 1, 1)
            game = self.generate_game()
            game.add_players(users)
            game.set_players_position()
            round.games.add(game)
            round.save()

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
        number_of_games = self.number_of_players / 2
        is_odd = self.number_of_players % 2
        rounds_base = self.number_of_players - 1 + is_odd
        repeatead_games = int(rounds_base / self.number_of_rounds)

        for i in range(repeatead_games):
            matches_scheduling = self.generate_matches_scheduling()

            for j in range(rounds_base):
                round_nbr = j + i * rounds_base + 1
                round = self.generate_round(round_nbr, number_of_games)
                for players_match in matches_scheduling[j]:
                    if all(p for p in players_match):
                        game = self.generate_game()
                        game.add_players(players_match)
                        game.set_players_position()
                        round.games.add(game)
                round.save()

    def generate_matches_scheduling(self) -> list[list[User | str]]:
        """
        Implements the scheduling algorithm for round robin tournament

        It rotates the players list for each round and gets the pairs for each match in
        the round:
        - the first element is always fixed in rotation
        - for each rotation, the last element goes to second place in the list and all
        other elements are moved one index forward
        """
        rotation = list(self._players.all())
        if self.number_of_players % 2:
            rotation.append(None)
        random.shuffle(rotation)

        # generate the rotated players list for each round
        rounds = []
        for i in range(0, len(rotation) - 1):
            rounds.append(rotation)
            rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

        # generate the pairs for each match
        scheduling = []
        for round in rounds:
            # scheduling.append(list[zip(*[iter(round)]*2)])
            scheduling.append(zip(*[iter(round)] * 2))

        return scheduling

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
    - maximum of 32 players
    - The number of rounds is n for 2 ** n = number_of_players
    """

    class Meta:
        proxy = True

    def generate_rounds(self, *args, **kwargs) -> None:
        perfect_players_number = int(math.pow(2, self.number_of_rounds))
        first_round_missing_players = perfect_players_number - self.number_of_players

        players_list = list(self._players.all())
        random.shuffle(players_list)  # blind
        players_list.extend([None] * first_round_missing_players)
        half = int(perfect_players_number / 2)
        players_pairs = list(zip(players_list[:half], players_list[half:]))

        rounds = []
        for i in range(self.number_of_rounds):
            number_of_games = int(math.pow(2, self.number_of_rounds - i - 1))
            # first round may be different

            round = Round.objects.create(
                round_number=(i + 1),
                number_of_games=number_of_games,
            )
            for j in range(number_of_games):
                game = Game.objects.create(
                    status=GameStatus.SCHEDULED,
                    rules=self.rules,
                )
                if i == 0:
                    # pprint(map(lambda p: game.add_player(p), players_pairs[j]))
                    game.set_players_position()
                round.games.add(game)

            self.rounds.add(round)
            rounds.append(round)

        # for round 1 and 2 we may add some players
        for players_match in players_pairs:
            game.add_players(players_match)
            game.set_players_position()
        # we also need to link the next game

    def validate_number_of_players(self, current_number_of_players: int):
        if current_number_of_players < 4:
            raise ValueError(
                "For Tournament Round Robin the number of players must be greater than"
                f"3, but {current_number_of_players} players were associated to it"
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
