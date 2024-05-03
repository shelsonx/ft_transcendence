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

        if players:
            for player in players:
                # game.players.add(player)
                self.seedGamePlayer(game=game, user=player)
        return game

    def gamePlayer(self, **fields) -> dict:
        game = fields.pop("game", None) or self.seedGame()
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
