# python std library
import uuid
from http import HTTPStatus

# Django
from django.http import (
    HttpRequest,
    HttpResponse,
    QueryDict,
)
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# First Party
from user.forms import UserSearchForm
from common.models import json_response
from core.models import (
    Game,
    GameRules,
    GameRuleType,
    GameStatus,
    Round,
    RoundStatus,
    Tournament,
    TournamentPlayer,
    TournamentStatus,
    TournamentType,
)
from core.forms import GameRulesForm, TournamentForm, TournamentPlayerForm
from user.decorators import JWTAuthentication
from user.models import User


@method_decorator(csrf_exempt, name="dispatch")  # remove csrf protection...
class AddTournamentView(generic.View):
    template_name = "add_tournament.html"
    tournament_form = None
    rules_form = None
    players_forms = None
    base_player_form = TournamentPlayerForm()

    @JWTAuthentication()
    def get(self, request: HttpRequest) -> HttpResponse:
        self.user = request.user
        self.set_forms()
        context = self.get_context_data()
        context["empty"] = True
        response = render(request, self.template_name, context)
        return response

    @JWTAuthentication()
    def post(self, request: HttpRequest) -> HttpResponse:
        self.user = request.user
        post_data = request.POST
        # self.set_forms(post_data)
        # context = self.get_context_data()
        # forms = [self.rules_form, self.user_form]

        # data = {"tournament": tournament.pk}
        return json_response.success(status=HTTPStatus.CREATED)

    def get_players(self, post_data: QueryDict) -> list[User]:
        usernames = post_data.getlist("username") if post_data else None
        players_list = [self.user]
        for username in usernames:
            user = User.get_object(username=username)
            players_list.append(user)
        return players_list

    def get_context_data(self, **kwargs) -> dict:
        return {
            # "invalid": False,
            "empty": False,
            "user": self.user,
            "type": TournamentType.ROUND_ROBIN,  # change
            "TournamentType": TournamentType,
            "rules_form": self.rules_form,
            "tournament_form": self.tournament_form,
            "players_forms": self.players_forms,
            "base_player_form": self.base_player_form,
        }

    def set_forms(self, data: QueryDict = None) -> None:
        self.rules_form = GameRulesForm(data)
        self.tournament_form = TournamentForm(data)

        if data:
            self.players_forms = []
            self.players = self.get_players(data)
            alias_names = data.getlist("alias_name")
            for i, p in enumerate(self.players):
                d = {"username": p.username, "alias_name": alias_names[i]}
                self.players_forms.append(TournamentPlayerForm(d))
            self.players_forms[0].fields["username"].disabled = True
        else:
            initial = {"username": self.user.username}
            owner_form = TournamentPlayerForm(initial=initial)
            owner_form.fields["username"].disabled = True
            self.players_forms = [owner_form]


class TournamentView(generic.View):
    template_name = "tournament.html"

    @JWTAuthentication()
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        self.tournament = Tournament.objects.filter(pk=pk).first()
        if not self.tournament:
            return json_response.not_found()

        self.tournament.is_owner = False
        if self.tournament.owner == request.user:
            self.tournament.is_owner = True

        response = render(request, self.template_name, self.get_context_data())
        return response

    @JWTAuthentication()
    def patch(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        tournament = Tournament.objects.filter(pk=pk).first()
        if not tournament:
            return json_response.not_found()
        if tournament.owner != request.user:
            return json_response.forbidden()

        # só pode mudar o status?
        # self.set_forms(request.POST)
        # context = self.get_context_data()
        # if not self.tournament_form.is_valid():  # or not self.rules_form.is_valid():
        #     return render(request, self.template_name, context)
        # return HttpResponseBadRequest()
        # tournament: Tournament = self.tournament_form.save()

        return json_response.success(msg="Tournament updated")

    @JWTAuthentication()
    def delete(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        tournament = Tournament.objects.filter(pk=pk).first()
        if not tournament:
            return json_response.not_found()
        if tournament.owner != request.user:
            return json_response.forbidden()

        tournament.delete()
        return json_response.success(msg="Tournament deleted")

    def get_context_data(self, **kwargs) -> dict:
        rounds = self.tournament.get_rounds()
        for r in rounds:
            r: Round
            r.ordered_games = r.games.all().order_by("game_datetime")
            for g in r.ordered_games:
                g: Game
                g.status_label = GameStatus(g.status).label

                player_left, player_right = g.players
                player_left.is_winner = False
                player_right.is_winner = False
                winner = g.winner
                if winner is not None:
                    if player_left and winner.pk == player_left.pk:
                        player_left.is_winner = True
                    else:
                        player_right.is_winner = True

                g.player_left = player_left
                g.player_right = player_right
                g.has_winner = bool(winner)

        self.tournament.status_label = TournamentStatus(self.tournament.status).label
        return {
            "t": self.tournament,
            "rounds": rounds,
            "TournamentStatus": TournamentStatus,
            "RoundStatus": RoundStatus,
        }
