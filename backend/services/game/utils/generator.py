import uuid
from datetime import timedelta
from random import randint

from django.utils import timezone

from backend.services.game.core.models.game_rules import GameRules
from user.models import User
from core.models import *


class Generator:
    def user(self, **fields):
        data = {
            "id": uuid.uuid4(),
            # "nickname": "nickname",
        }
        data.update(**fields)

        return data

    def seedUser(self, **fields) -> User:
        return User.objects.create(**(self.user(**fields)))

    def game_rules(self, **fields):
        data = {
            "player_reach_points": randint(5, 11),
        }
        data.update(**fields)

        return data

    def seedGameRules(self, **fields):
        return GameRules.objects.create(self.user(**fields))

    def game(self, **fields):
        player_a = fields.get("player_a") or self.seedUser()
        player_b = fields.get("player_b") or self.seedUser()

        data = {
            "game_datetime": timezone.now(),
            "status": GameStatus.ENDED,
            "duration": timedelta(minutes=randint(1, 5), seconds=randint(0, 59)),
            "player_a": player_a,
            "player_b": player_b,
            "score_a": randint(0, 11),
            "score_b": randint(0, 11),
        }
        data.update(**fields)

        return data

    def seedGame(self, **fields):
        return User.objects.create(self.user(**fields))
