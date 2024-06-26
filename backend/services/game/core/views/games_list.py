# Create your views here.
# Standard Library
from datetime import timedelta
import logging

# import pprint
import uuid

# Third Party
from django.db.models import Q, Sum
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import resolve

# from django.utils.translation import gettext_lazy as _
from django.views import generic

from common.models import json_response
from core.models import Game, GamePlayer, GameStatus, TournamentPlayer, TournamentStatus
from user.decorators import JWTAuthentication
from user.models import User

logger = logging.getLogger("eqlog")


class GamesView(generic.ListView):
    model = Game
    ordering = ["-game_datetime", "status"]
    template_name = "games_list.html"
    is_public_view = False
    # paginate_by = 20
    excluded_status = [
        GameStatus.PENDING,
        GameStatus.SCHEDULED,
        GameStatus.CANCELED,
        GameStatus.TOURNAMENT,
    ]

    @JWTAuthentication()
    def get(
        self, request: HttpRequest, pk: uuid = None, *args, **kwargs
    ) -> HttpResponse:
        self.user = None
        if pk:
            self.user = User.get_object(pk=pk)
            if not self.user:
                return json_response.not_found()

            current_url = resolve(request.path_info).url_name
            if current_url == "view_user_games":
                self.is_public_view = True
            elif self.user != request.user:
                return json_response.forbidden()

        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Game]:
        if self.user and not self.is_public_view:
            return (
                self.user.games.all()
                .exclude(Q(status__in=self.excluded_status) & ~Q(owner=self.user))
                .exclude(status=GameStatus.TOURNAMENT)
            )
        elif self.user:
            return self.user.games.all().exclude(status__in=self.excluded_status)

        queryset = super().get_queryset()
        return queryset.exclude(status__in=self.excluded_status)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["user"] = self.user
        context["is_public_view"] = self.is_public_view
        context["GameStatus"] = GameStatus

        game_list = []
        count = 0
        for game in context["game_list"]:
            game_list.append(self.get_game_data(game))
            count += 1
        context["game_list"] = game_list
        context["total_games"] = count

        if self.user:
            all_users = User.objects.all().order_by("rating")
            for i, u in enumerate(all_users):
                if u == self.user:
                    self.user.rank = i + 1
                    break

            tps = TournamentPlayer.objects.filter(
                user=self.user, tournament__status=TournamentStatus.ENDED
            )
            self.user.tournaments_count = tps.count()
            self.user.tournaments_points = tps.aggregate(total=Sum("score"))["total"]

            gps = GamePlayer.objects.filter(
                user=self.user, game__status=GameStatus.ENDED
            ).order_by("-score")
            self.user.max_points = gps.first().score if gps.exists() else "-"

            games = self.user.games.filter(status=GameStatus.ENDED).order_by(
                "-duration"
            )
            self.user.longest_game = games.first().duration if games.exists() else "-"
            self.user.fastest_game = games.last().duration if games.exists() else "-"

        return context

    def get_game_data(self, game: Game) -> Game:
        game.status_label = GameStatus(game.status).label

        player_left, player_right = game.players
        player_left.is_winner = False
        player_right.is_winner = False
        winner = game.winner
        if winner is not None:
            if player_left and winner.pk == player_left.pk:
                player_left.is_winner = True
            else:
                player_right.is_winner = True

        game.player_left = player_left
        game.player_right = player_right
        game.has_winner = bool(winner)

        game.is_owner = False
        if self.user and game.owner and self.user.pk == game.owner.pk:
            game.is_owner = True

        game.is_winner = False
        if winner and winner.user and self.user and winner.user.pk == self.user.pk:
            game.is_winner = True

        game.tournament = None
        round = game.round.all().first()
        if round:
            game.tournament = round.tournament

        game.game_datetime -= timedelta(hours=3)

        return game
