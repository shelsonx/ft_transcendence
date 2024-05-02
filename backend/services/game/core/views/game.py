# Create your views here.
# Standard Library
import logging
from datetime import timedelta

# Third Party
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic

from core.models import Game, GameStatus
from user.models import User

logger = logging.getLogger("eqlog")


# class GameView(generic.View):
# class GameView(generic.ListView):
class GameView(generic.DetailView):
    template_name = "game.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        game = Game(
            game_datetime=timezone.now(),
            status=GameStatus.SCHEDULED,
            duration=timedelta(minutes=5, seconds=33),
            player_a=User(id_reference=1),
            player_b=User(id_reference=2),
        )

        context = {
            "game": game,
        }
        response = render(request, self.template_name, context)
        return response
