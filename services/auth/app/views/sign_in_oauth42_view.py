import json
from typing import Any
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views import View

from ..interfaces.services.http_client import IHttpClient
from ..interfaces.controllers.base_oauth42_controller import BaseOAuth42Controller
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..dtos.access_token_42 import AccessToken42
import os
from ..interfaces.usecase.base_usecase import BaseUseCase


@method_decorator(csrf_exempt, name="dispatch")
class SignInOAuth42View(View):
    sign_in_oauth42_controller: BaseOAuth42Controller = None

    def __init__(self, sign_in_oauth42_controller: BaseOAuth42Controller) -> None:
        self.sign_in_oauth42_controller = sign_in_oauth42_controller

    async def get(self, request: HttpRequest) -> JsonResponse:
        return await self.sign_in_oauth42_controller.handle_callback(request)
