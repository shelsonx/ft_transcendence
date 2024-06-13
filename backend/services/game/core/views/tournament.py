# python std library
import uuid
from http import HTTPStatus

# Django
from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
    HttpResponseBadRequest,
)
from django.shortcuts import get_object_or_404, render
from django.views import generic

# First Party
from core.models import (
    Game,
    GameStatus,
    GameRules,
    GameRuleType,
    Tournament,
    TournamentStatus,
    TournamentType,
)
from core.forms import GameForm, GameEditForm, GameRulesForm
from user.decorators import JWTAuthentication
from user.models import User


class TournamentView(generic.View):
    template_name = "tournament.html"
    tournament = None
    tournament_form = None
    rules_form = None

    @JWTAuthentication()
    def get(self, request: HttpRequest, pk: int = None) -> HttpResponse:
        if pk:
            self.tournament = get_object_or_404(Tournament, pk=pk)
        else:
            self.set_forms()

        response = render(request, self.template_name, self.get_context_data())
        return response

    @JWTAuthentication()
    def post(self, request: HttpRequest) -> HttpResponse:
        # TODO: SHEELA - verify if all users exists
        # remove this:
        from utils.generator import Generator

        gen = Generator()
        tournament = gen.seedTournament()
        # player_a = gen.seedUser()
        # player_b = gen.seedUser()

        # self.set_forms(request.POST)
        # context = self.get_context_data()
        # if not self.tournament_form.is_valid() or not self.rules_form.is_valid():
        #     return render(request, self.template_name, context)

        # rules: GameRules = self.rules_form.save()
        # # lógica para não duplicar regras!!
        # tournament: Game = self.tournament_form.save(commit=False)
        # tournament.rules = rules
        # tournament.save()

        # tournament.players.add(player_a)
        # tournament.players.add(player_b)

        print("Tournament created: ", tournament)
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    @JWTAuthentication()
    def patch(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        # TODO: SHEELA - protect route
        self.tournament = get_object_or_404(Tournament, pk=pk)
        # verificar acesso ao jogo

        # a edição na verdade vai seguir outras regras... salvar scores, status
        self.set_forms(request.POST)
        context = self.get_context_data()
        # if not self.tournament_form.is_valid():  # or not self.rules_form.is_valid():
        #     return render(request, self.template_name, context)
            # return HttpResponseBadRequest()

        # tournament: Tournament = self.tournament_form.save()
        print("Tournament updated: ", self.tournament)
        return render(request, self.template_name, context)
        # return HttpResponse(status=HTTPStatus.NO_CONTENT)

    # TODO: SHEELA - protect route to only gateway
    @JWTAuthentication()
    def delete(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        # TODO: SHEELA - protect route
        tournament = get_object_or_404(Tournament, pk=pk)
        tournament.delete()
        print("tournament deleted: ", tournament)
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    def get_context_data(self, **kwargs) -> dict:
        return {
            "tournament": self.tournament,
            "TournamentStatus": TournamentStatus,
            "tournament_form": self.tournament_form,
            "rules_form": self.rules_form,
        }

    def set_forms(self, data=None) -> None:
        initial = {
            # "status": TournamentStatus.INVITATION,
            "status": GameStatus.PENDING,
        }
        self.tournament_form = GameForm(data, initial=initial, instance=self.tournament)
        self.rules_form = GameRulesForm(data)
