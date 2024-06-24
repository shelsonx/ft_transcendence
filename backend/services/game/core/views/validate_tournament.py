# python std library
import json
import uuid

# Django
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

# First Party
from common.models import json_response
from user.decorators import JWTAuthentication
from core.models import (
    Game,
    GameStatus,
    Round,
    RoundStatus,
    Tournament,
    TournamentPlayer,
    TournamentStatus,
    TournamentType,
)
from core.forms import PlayerValidationForm


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
            p.form = PlayerValidationForm(initial=initial)

        context = {
            "t": t,
            "players": players,
            "TournamentType": TournamentType,
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

        data = json.loads(request.body)
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

        auth_data = data.get("auth_data")
        if not auth_data:
            return json_response.bad_request("missing auth data")

        is_valid = auth_data.get("is_success")
        status = auth_data.get("status")
        if not is_valid and status == 400:
            form = PlayerValidationForm(data)
            form.is_valid()
            form.add_error("token", auth_data.get("error"))

            players = t.players
            for p in players:
                if p != player:
                    initial = {"user": p.user.id if p.user else None}
                    p.form = PlayerValidationForm(initial=initial)
                else:
                    p.form = form

            context = {
                "t": t,
                "players": players,
                "TournamentType": TournamentType,
            }
            return render(request, self.template_name, context)

        player.verified = True
        player.save()

        if not all(p.verified for p in t.players):
            return self.get(request, pk)

        t.status = TournamentStatus.SCHEDULED
        t.tournament_date = timezone.now().date()
        t.save()
        t.generate_rounds()
        first_round: Round = t.get_rounds().first()
        first_game: Game = first_round.get_next_or_current_game()
        first_round.status = RoundStatus.ON_GOING
        first_game.status = GameStatus.SCHEDULED
        first_round.save()
        first_game.save()

        return json_response.success(msg="Tournament validated")
