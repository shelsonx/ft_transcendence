# Create your views here.
# Standard Library
from datetime import timedelta
import logging
import uuid

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
        )
        # game.players.add(User(id=uuid.uuid4))
        # game.players.add(User(id=uuid.uuid4))

        context = {
            "game": game,
        }
        response = render(request, self.template_name, context)
        return response
