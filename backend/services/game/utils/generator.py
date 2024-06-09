import pprint
import uuid
from datetime import timedelta
from random import randint

from django.utils import timezone

from user.models import User
from core.models import *


class Generator:
    def user(self, **fields) -> dict:
        data = {
            "id": uuid.uuid4(),
            # "nickname": "nickname",
        }
        data.update(**fields)

        return data

    def seedUser(self, **fields) -> User:
        return User.objects.create(**(self.user(**fields)))

    def seedGameRules(self, **fields) -> GameRules:
        rules = None
        size = len(fields)
        if size >= 1:
            rules = GameRules.objects.filter(**fields).first()

        if rules:
            return rules

        if size >= 2 or (size == 1 and fields.get("points_to_win")):
            # TODO: talvez passar um full clean?
            return GameRules.objects.create(**fields)

        return GameRules.objects.get(pk=1)

    def game(self, **fields) -> dict:
        data = {
            "game_datetime": timezone.now(),
            "status": GameStatus.ENDED,
            "duration": timedelta(minutes=randint(1, 5), seconds=randint(0, 59)),
            "rules": self.seedGameRules(),
        }
        data.update(**fields)

        return data

    def seedGame(self, **fields) -> Game:
        players = fields.pop("players", None) or [self.seedUser(), self.seedUser()]
        game = Game.objects.create(**(self.game(**fields)))
        game.add_players(players)

        if not game.owner:
            game.owner = players[0]
            game.save()
        game.set_players_position()
        return game

    def gamePlayer(self, **fields) -> dict:
        game = fields.pop("game", None)
        if not game:
            raise ValueError("you need to pass the game")

        user = fields.pop("user", None) or self.seedUser()
        score = 0
        if game.status in [GameStatus.ENDED, GameStatus.ONGOING]:
            score = randint(1, game.rules.points_to_win or 21)

        data = {
            "game": game,
            "user": user,
            "score": score,
        }

        data.update(**fields)
        return data

    def seedGamePlayer(self, **fields) -> GamePlayer:
        data = self.gamePlayer(**fields)
        return GamePlayer.objects.create(**data)

    def tournament(self, **fields) -> dict:
        rules = fields.pop("rules", None) or self.seedGameRules()
        data = {
            "tournament_type": TournamentType.CHALLENGE,
            "status": TournamentStatus.INVITATION,
            "tournament_date": timezone.now().date() - timedelta(days=15),
            "rules": rules,
            "number_of_players": 2,
            "number_of_rounds": 3,
        }
        data.update(**fields)
        return data

    def seedTournament(self, **fields) -> Tournament:
        players = fields.pop("players", None)
        tournament = Tournament.objects.create(**(self.tournament(**fields)))

        if players and len(players) != tournament.number_of_players:
            raise ValueError(
                "mismatch in players sent and tournament's number of players"
            )

        if players is None:
            players = []
            for _ in range(tournament.number_of_players):
                players.append(self.seedUser())

        for player in players:
            # tournament.players.add(player)
            self.seedTournamentPlayer(tournament=tournament, user=player)

        if not tournament.owner:
            tournament.owner = players[0]
            tournament.save()
        tournament.generate_rounds()
        return tournament

    def tournamentPlayer(self, **fields) -> dict:
        tournament = fields.pop("tournament", None)
        if not tournament:
            raise ValueError("you need to pass the tournament")

        user = fields.pop("user", None) or self.seedUser()
        data = {
            "tournament": tournament,
            "user": user,
            "alias_name": "alias_name",
            "score": 0,
            "rating": 0,
        }

        data.update(**fields)
        return data

    def seedTournamentPlayer(self, **fields) -> TournamentPlayer:
        data = self.tournamentPlayer(**fields)
        return TournamentPlayer.objects.create(**data)
