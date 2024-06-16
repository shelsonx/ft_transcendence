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
    GameRules,
    GameRuleType,
    Tournament,
    TournamentStatus,
    TournamentType,
)
from core.forms import GameRulesForm, TournamentForm
from user.decorators import JWTAuthentication
from user.models import User

@method_decorator(csrf_exempt, name="dispatch")  # remove csrf protection...
class AddTournamentView(generic.View):
    template_name = "add_tournament.html"
    tournament_form = None
    rules_form = None
    users_form = []

    @JWTAuthentication()
    def get(self, request: HttpRequest) -> HttpResponse:
        self.set_forms()
        response = render(request, self.template_name, self.get_context_data())
        return response

    @JWTAuthentication()
    def post(self, request: HttpRequest) -> HttpResponse:
        post_data = request.POST
        self.set_forms(post_data)
        context = self.get_context_data()
        forms = [self.rules_form, self.user_form]

        data = {"status": "success", "data": {"tournament": "tournament"}}
        return json_response.success(data=data, status=HTTPStatus.CREATED)

    def get_players(self, post_data: QueryDict | None) -> list[User]:
        players = post_data.getlist("username") if post_data else None
        players_list = []
        for p in players:
            p = User.get_object(username=p)
        return players_list

    def get_context_data(self, **kwargs) -> dict:
        return {
            "invalid": False,
            "TournamentStatus": TournamentStatus,
            "rules_form": self.rules_form,
            "tournament_form": self.tournament_form,
            "users_form": self.users_form,
        }

    def set_forms(self, data=None) -> None:
        self.rules_form = GameRulesForm(data)
        self.tournament_form = TournamentForm(data)

        if data:
            self.players = self.get_players(data)
            for p in self.players:
                self.users_form.append(UserSearchForm(data, instance=self.players))


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
        return {
            "tournament": self.tournament,
            "TournamentStatus": TournamentStatus,
        }
