import uuid
from datetime import timedelta
from random import randint

from django.utils import timezone

from backend.services.game.core.models.match_rules import MatchRules
from user.models import User
from core.models import *


class Generator:
    def user(self, **fields):
        data = {
            "id_reference": uuid.uuid4(),
        }
        data.update(**fields)

        return data

    def seedUser(self, **fields):
        return User.objects.create(self.user(**fields))

    def match_rules(self, **fields):
        data = {
            "player_reach_points": randint(5, 11),
        }
        data.update(**fields)

        return data

    def seedMatchRules(self, **fields):
        return MatchRules.objects.create(self.user(**fields))

    def match(self, **fields):
        player_a = fields.get("player_a") or self.seedUser()
        player_b = fields.get("player_b") or self.seedUser()

        data = {
            "match_datetime": timezone.now(),
            "status": MatchStatus.ENDED,
            "duration": timedelta(minutes=randint(1, 5), seconds=randint(0, 59)),
            "player_a": player_a,
            "player_b": player_b,
            "score_a": randint(0, 11),
            "score_b": randint(0, 11),
        }
        data.update(**fields)

        return data

    def seedMatch(self, **fields):
        return User.objects.create(self.user(**fields))
