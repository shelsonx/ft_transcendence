# python std library
from http import HTTPStatus

# Django
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

# First Party
from common.models import json_response
from user.decorators import JWTAuthentication
from core.models import Game, GameStatus
from core.forms import GameValidationForm


@method_decorator(csrf_exempt, name="dispatch")
class ValidateGameView(generic.View):
    template_name = "game/validate.html"

    @JWTAuthentication()
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        game = Game.objects.filter(pk=pk).first()
        if not game:
            return json_response.not_found()
        if game.owner != request.user:
            return json_response.forbidden()

        left, right = game.players
        player_to_validate = right if game.owner == left else right
        if not player_to_validate.user:
            return json_response.not_found()

        context = {
            "game": game,
            "form": GameValidationForm(),
            "user": player_to_validate.user,
            "GameStatus": GameStatus,
        }
        response = render(request, self.template_name, context)
        return response

    @JWTAuthentication()
    def patch(self, request: HttpRequest, pk: int) -> HttpResponse:
        game = Game.objects.filter(pk=pk).first()
        if not game:
            return json_response.not_found()
        if game.owner != request.user:
            return json_response.forbidden()
        if game.status != GameStatus.PENDING:
            return json_response.bad_request()

        left, right = game.players
        player_to_validate = right if game.owner == left else right
        if not player_to_validate.user:
            return json_response.not_found()

        data = QueryDict(request.body)
        form = GameValidationForm(data)
        if not form.is_valid():
            context = {
                "game": game,
                "form": form,
                "user": player_to_validate.user,
                "GameStatus": GameStatus,
            }
            return render(request, self.template_name, context)

        # TODO: verificação do token - Bruno

        game.status = GameStatus.SCHEDULED
        game.save()
        return json_response.success(msg="Game validated")
