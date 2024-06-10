# Create your views here.
# Standard Library
import logging
# import pprint
import uuid

# Third Party
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
# from django.utils.translation import gettext_lazy as _
from django.views import generic

from core.models import Game, GameStatus
from common.decorators import logged_permission
from user.models import User

logger = logging.getLogger("eqlog")


class GamesView(generic.ListView):
    model = Game
    ordering = ["-game_datetime", "status"]
    template_name = "games_table.html"
    # paginate_by = 20

    # TODO SHEELA: proteger a rota - somente o usuário pode acessar?
    @logged_permission()
    def get(
        self, request: HttpRequest, pk: uuid = None, *args, **kwargs
    ) -> HttpResponse:
        # pprint.pprint(request, indent=4)
        # pprint.pprint(request.headers, indent=4)
        self.user = None
        if pk:
            self.user = User.objects.filter(pk=pk).first()  # TODO: usar a regra abaixo
            if not self.user:
                self.user = get_object_or_404(User, username="sheela")
            # self.user = get_object_or_404(User, pk=pk)
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Game]:
        if self.user:
            return self.user.games.all()

        excluded_status = [
            GameStatus.PENDING,
            GameStatus.SCHEDULED,
            GameStatus.CANCELED,
        ]
        queryset = super().get_queryset()
        return queryset.exclude(status__in=excluded_status)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        context["GameStatus"] = GameStatus

        game_list = []
        for game in context["game_list"]:
            game_list.append(self.get_game_data(game))
        context["game_list"] = game_list

        return context

    def get_game_data(self, game: Game) -> Game:
        game.status_label = GameStatus(game.status).label

        player_left, player_right = game.players
        player_left.is_winner = False
        player_right.is_winner = False
        winner = game.winner
        if winner and winner.pk == player_left.user.pk:
            player_left.is_winner = True
        else:
            player_right.is_winner = True
        game.player_left = player_left
        game.player_right = player_right

        return game
