from django.db import models
from django.utils.translation import gettext_lazy as _


class TournamentType(models.IntegerChoices):
    CHALLENGE = 0, _("Challenge")  # e.g: best of 3
    ROUND_ROBIN = 1, _("Round-robin")  # pontos corridos
    # ELIMINATION = 2, _("Elimination")  # mata-mata
    # LEAGUE_WITH_PLAYOFF = 3, _("League with Playoff")  # mix
