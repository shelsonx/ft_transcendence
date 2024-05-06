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
from django.utils.decorators import method_decorator
from django.views import generic

# First Party
from core.models import Game, GameStatus, GameRules, GameRuleType
from core.forms import GameForm, GameEditForm, GameRulesForm
from user.decorators import logged_permission
from user.models import User


class GameView(generic.View):
    template_name = "game.html"
    game = None
    game_form = None
    rules_form = None

    @logged_permission()
    def get(self, request: HttpRequest, pk: int = None) -> HttpResponse:
        if pk:
            self.game = get_object_or_404(pk=pk)
        else:
            self.set_forms()

        response = render(request, self.template_name, self.get_context_data())
        return response

    @logged_permission()
    def post(self, request: HttpRequest) -> HttpResponse:
        # TODO: SHEELA - verify if users exists
        # player_a = get_object_or_404(User)
        # player_b = get_object_or_404(User)
        # remove this:
        from utils.generator import Generator

        gen = Generator()
        player_a = gen.seedUser()
        player_b = gen.seedUser()

        self.set_forms(request.POST)
        context = self.get_context_data()
        if not self.game_form.is_valid() or not self.rules_form.is_valid():
            return render(request, self.template_name, context)

        rules: GameRules = self.rules_form.save()
        # lógica para não duplicar regras!!
        game: Game = self.game_form.save(commit=False)
        game.rules = rules
        game.save()

        game.players.add(player_a)
        game.players.add(player_b)

        print("Game created: ", game)
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    @logged_permission()
    def patch(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        # TODO: SHEELA - protect route
        self.game = get_object_or_404(Game, pk=pk)
        # verificar acesso ao jogo

        # a edição na verdade vai seguir outras regras... salvar scores, status
        self.set_forms(request.POST)
        context = self.get_context_data()
        if not self.game_form.is_valid():  # or not self.rules_form.is_valid():
            return render(request, self.template_name, context)
            # return HttpResponseBadRequest()

        game: Game = self.game_form.save()
        print("Game updated: ", game)
        return render(request, self.template_name, context)
        # return HttpResponse(status=HTTPStatus.NO_CONTENT)

    # TODO: SHEELA - protect route to only gateway
    @logged_permission()
    def delete(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        # TODO: SHEELA - protect route
        game = get_object_or_404(Game, pk=pk)
        game.delete()
        print("game deleted: ", game)
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    def get_context_data(self, **kwargs) -> dict:
        return {
            "game": self.game,
            "GameStatus": GameStatus,
            "game_form": self.game_form,
            "rules_form": self.rules_form,
        }

    def set_forms(self, data=None) -> None:
        initial = {
            "status": GameStatus.PENDING,
        }
        self.game_form = GameForm(data, initial=initial, instance=self.game)
        self.rules_form = GameRulesForm(data)
