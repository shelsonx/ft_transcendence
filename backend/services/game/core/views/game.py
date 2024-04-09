# Create your views here.
# Standard Library
import logging

# Third Party
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import generic

logger = logging.getLogger("eqlog")


class GameView(generic.View):
    template_name = "game.html"

    def get(self, request: HttpRequest) -> HttpResponse:

        context = {
            "game": "GAME",
        }
        response = render(request, self.template_name, context)
        return response

