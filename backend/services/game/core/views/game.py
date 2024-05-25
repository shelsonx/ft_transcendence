# python std library
import pprint
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
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

# First Party
from core.models import Game, GameStatus, GameRules, GameRuleType
from core.forms import GameForm, GameEditForm, GameRulesForm
from common.decorators import logged_permission
from user.forms import UserSearchForm
from user.models import User


@method_decorator(csrf_exempt, name="dispatch")  # remove csrf protection...
class AddGameView(generic.View):
    template_name = "add_game.html"
    game_form = None
    rules_form = None
    user_form = None

    # @csrf_protect
    @logged_permission()
    def get(self, request: HttpRequest) -> HttpResponse:
        pprint.pprint(request, indent=4)
        print("Cookies: ", request.COOKIES)
        self.set_forms()

        response = render(request, self.template_name, self.get_context_data())
        return response

    # @csrf_protect
    @logged_permission()
    def post(self, request: HttpRequest) -> HttpResponse:
        # TODO: SHEELA - verify if users exists
        # player_a = get_object_or_404(User)
        # player_b = get_object_or_404(User)
        # remove this:
        print("entrou no post")
        from utils.generator import Generator

        gen = Generator()
        player_a = gen.seedUser(username="user21")
        player_b = gen.seedUser(username="user42")

        self.set_forms(request.POST)
        context = self.get_context_data()
        if not self.rules_form.is_valid():
            context["invalid"] = True
            return render(request, self.template_name, context)

        rules: GameRules = self.rules_form.save()
        # lógica para não duplicar regras!!
        game: Game = self.game_form.save(commit=False)
        game.rules = rules
        game.save()

        game.players.add(player_a)
        game.players.add(player_b)

        print("Game created: ", game)
        # we need to show
        # confirm_template =
        # response = render(request, self.template_name, self.get_context_data())
        # return response
        data = {"status": "success", "data": {"game": game.pk}}
        return JsonResponse(data, status=HTTPStatus.CREATED)

    def get_context_data(self, **kwargs) -> dict:
        return {
            "invalid": False,
            "GameStatus": GameStatus,
            "game_form": self.game_form,
            "rules_form": self.rules_form,
            "user_form": self.user_form,
        }

    def set_forms(self, data=None) -> None:
        initial = {
            "status": GameStatus.PENDING,
        }
        self.game_form = GameForm(data, initial=initial)
        self.rules_form = GameRulesForm(data)
        self.user_form = UserSearchForm(data)


class GameView(generic.View):
    @logged_permission()
    def get(self, request: HttpRequest, pk: int = None) -> HttpResponse:
        game = Game.objects.filter(pk=pk).first()
        if not game:
            return JsonResponse({"status": "not found"}, status=HTTPStatus.NOT_FOUND)
        # verificar se o usuário é o dono do jogo, se tem acesso?

        data = {"status": "success", "data": {"game": game.to_json()}}
        return JsonResponse(data, status=HTTPStatus.OK)

    # @csrf_protect
    # @logged_permission()
    # def patch(self, request: HttpRequest, pk: uuid) -> HttpResponse:
    #     # TODO: SHEELA - protect route
    #     self.game = get_object_or_404(Game, pk=pk)
    #     # verificar acesso ao jogo

    #     # a edição na verdade vai seguir outras regras... salvar scores, status
    #     self.set_forms(request.POST)
    #     context = self.get_context_data()
    #     if not self.game_form.is_valid():  # or not self.rules_form.is_valid():
    #         return render(request, self.template_name, context)
    #         # return HttpResponseBadRequest()

    #     game: Game = self.game_form.save()
    #     print("Game updated: ", game)
    #     return render(request, self.template_name, context)
    # return HttpResponse(status=HTTPStatus.NO_CONTENT)

    # TODO: SHEELA - protect route to only gateway
    @csrf_protect
    @logged_permission()
    def delete(self, request: HttpRequest, pk: uuid) -> HttpResponse:
        # TODO: SHEELA - protect route
        game = get_object_or_404(Game, pk=pk)
        game.delete()
        print("game deleted: ", game)
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
