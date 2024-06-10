# python std library
import pprint
import random
import uuid
from http import HTTPStatus
import logging

# Django
from django.forms import ValidationError
from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
    QueryDict,
)
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

# First Party
from common.middlewares import JWTAuthenticationMiddleware
from core.models import Game, GameStatus, GameRules
from core.forms import GameForm, GameEditForm, GameRulesForm
from common.decorators import logged_permission
from user.forms import UserSearchForm
from user.models import User


@method_decorator(csrf_exempt, name="dispatch")  # remove csrf protection...
class AddGameView(generic.View):
    template_name = "add_game.html"
    rules_form = None
    user_form = None

    # @csrf_protect
    # @JWTAuthenticationMiddleware(func=User.validate_user_id)\
    def get(self, request: HttpRequest) -> HttpResponse:
        pprint.pprint(request, indent=4)
        print("Cookies: ", request.COOKIES)
        self.set_forms()

        response = render(request, self.template_name, self.get_context_data())
        return response

    # @JWTAuthenticationMiddleware(func=User.validate_user_id)
    # @logged_permission()
    # @csrf_protect
    def post(self, request: HttpRequest) -> HttpResponse:
        # request_user = request.current_user
        # TODO: pedir o usuário para Lili ou Bruno e salvar se existir
        request_user = User.objects.get(username="sheela")
        pprint.pprint(request.POST, indent=4)
        # pprint.pprint(request.headers, indent=4)

        post_data = request.POST
        self.set_forms(post_data)
        context = self.get_context_data()
        forms = [self.rules_form, self.user_form]
        if not self.opponent:
            [form.is_valid() for form in forms]
            self.user_form.add_error(
                "username", ValidationError(message="user does not exist")
            )
            return render(request, self.template_name, context)
        if not all(form.is_valid() for form in forms):
            # context["invalid"] = True
            return render(request, self.template_name, context)

        rules: GameRules = GameRules.filter(self.rules_form)
        if rules is None:
            rules = self.rules_form.save()
        data = {
            "status": GameStatus.SCHEDULED,  # TODO: deixar como PENDING
            "rules": rules,
        }
        game_form = GameForm(data)
        if not game_form.is_valid():
            message = _("An internal error occured while creating the game")
            log = message + ": " + game_form.errors.as_text()
            logging.error(log)
            return HttpResponse(message, status=HTTPStatus.INTERNAL_SERVER_ERROR)

        game: Game = game_form.save(commit=False)
        game.owner = request_user
        game.save()
        game.add_player(request_user)
        game.add_player(self.opponent)
        game.set_players_position()

        data = {"status": "success", "data": {"game": game.pk}}
        return JsonResponse(data, status=HTTPStatus.CREATED)

    def get_opponent(self, post_data: QueryDict | None) -> User | None:
        opponent = post_data.get("username") if post_data else None
        if opponent:
            opponent = User.objects.filter(username=opponent).first()
        # if not opponent:
        # TODO: pedir o usuário para Lili ou Bruno e salvar se existir
        return opponent

    def get_context_data(self, **kwargs) -> dict:
        return {
            "invalid": False,
            "GameStatus": GameStatus,
            "rules_form": self.rules_form,
            "user_form": self.user_form,
        }

    def set_forms(self, data=None) -> None:
        self.opponent = self.get_opponent(data)
        print(self.opponent)
        self.rules_form = GameRulesForm(data)
        self.user_form = UserSearchForm(data, instance=self.opponent)


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
