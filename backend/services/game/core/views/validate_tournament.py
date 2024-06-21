# python std library
from http import HTTPStatus
import uuid

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
from core.models import Tournament, TournamentPlayer, TournamentStatus
from core.forms import TournamentValidationForm


@method_decorator(csrf_exempt, name="dispatch")
class ValidateTournamentView(generic.View):
    template_name = "tournament/validate.html"

    @JWTAuthentication()
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        t = Tournament.objects.filter(pk=pk).first()
        if not t:
            return json_response.not_found()
        if t.owner != request.user:
            return json_response.forbidden()
        if t.status != TournamentStatus.INVITATION:
            return json_response.bad_request()

        players = t.players
        for p in players:
            initial = {"user": p.user.id if p.user else None}
            p.form = TournamentValidationForm(initial=initial)

        context = {
            "t": t,
            "players": players,
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

        data = QueryDict(request.body)
        player = data.get("player")
        user_id = data.get("user")
        if not player or not user_id:
            return json_response.bad_request()
        player = TournamentPlayer.objects.filter(pk=player).first()
        if not player:
            return json_response.not_found()
        if player.verified or not player.user:
            return json_response.bad_request()

        user_id = uuid.UUID(user_id)
        if player.user.id != user_id:
            return json_response.bad_request()

        data = {
            "user": player.user.id,
            "token": data["token"],
        }
        form = TournamentValidationForm(data)
        if not form.is_valid():
            players = t.players
            for p in players:
                if p != player:
                    initial = {"user": p.user.id if p.user else None}
                    p.form = TournamentValidationForm(initial=initial)
                else:
                    p.form = form
            context = {
                "t": t,
                "players": players,
            }
            return render(request, self.template_name, context)

        # TODO: verificação do token - Bruno
        player.verified = True
        player.save()

        if not all(p.verified for p in t.players):
            print("entrou")
            return self.get(request, pk)

        t.status = TournamentStatus.SCHEDULED
        t.save()
        t.generate_rounds()
        return json_response.success(msg="Tournament validated")
