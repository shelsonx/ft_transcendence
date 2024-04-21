from django.db import models
from itertools import chain
import uuid

# Create your models here.

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_reference = models.UUIDField(editable=False, default=uuid.uuid4)

    @property
    def matchs(self) -> list:
        matchs_as_player_a = self.matchs_a.all()
        matchs_as_player_b = self.matchs_b.all()
        matchs = list(chain(matchs_as_player_a, matchs_as_player_b))

        return matchs
