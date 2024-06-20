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
from core.models import Game, GameStatus, VerificationType, Tournament, TournamentStatus
from core.forms import ValidationForm
from user.models import User


@method_decorator(csrf_exempt, name="dispatch")
class ValidateTournamentView(generic.View):
    template_name = "tournament/validate.html"

    @JWTAuthentication()
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        t = Tournament.objects.filter(pk=pk).first()
        if not t:
            return json_response.not_found()
        # if t.owner != request.user:
        #     return json_response.forbidden()
        # if t.status != TournamentStatus.INVITATION:
        #     return json_response.bad_request()

        # left, right = game.players
        # player_to_validate = right if game.owner == left else right
        # if not player_to_validate.user:
        #     return json_response.not_found()

        context = {
            "tournament": t,
            "form": ValidationForm(),
            # "user": player_to_validate.user,
        }
        response = render(request, self.template_name, context)
        return response

    @JWTAuthentication()
    def patch(self, request: HttpRequest, pk: int) -> HttpResponse:
        t = Tournament.objects.filter(pk=pk).first()
        if not t:
            return json_response.not_found()
        if t.owner != request.user:
            return json_response.forbidden()
        if t.status != TournamentStatus.INVITATION:
            return json_response.bad_request()

        # left, right = game.players
        # player_to_validate = right if game.owner == left else right
        # if not player_to_validate.user:
        #     return json_response.not_found()

        data = QueryDict(request.body)
        form = ValidationForm(data)
        if not form.is_valid():
            context = {
                "tournament": t,
                # "form": form,
                # "user": player_to_validate.user,
            }
            return render(request, self.template_name, context)

        # TODO: verificação do token - Bruno
        # player.is_verified = True
        # player.save()

        # se todos os jogadores estiverem validados:
        # t.status = GameStatus.SCHEDULED
        # t.save()
        return json_response.success(msg="Tournament validated")
        # caso contrário, devolve a página com o status atualizado