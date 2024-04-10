from django.db import models
from itertools import chain

# Create your models here.

class User(models.Model):
    id_reference = models.IntegerField()

    @property
    def matchs(self) -> list:
        matchs_as_player_a = self.matchs_a.all()
        matchs_as_player_b = self.matchs_b.all()
        matchs = list(chain(matchs_as_player_a, matchs_as_player_b))

        return matchs
