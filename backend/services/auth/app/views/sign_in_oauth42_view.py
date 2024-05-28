import json
from typing import Any
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.views import View
from ..interfaces.controllers.base_oauth42_controller import BaseOAuth42Controller
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..constants.oauth_urls import OAuthUrls
from ..interfaces.usecase.base_usecase import BaseUseCase
from django.shortcuts import redirect


@method_decorator(csrf_exempt, name="dispatch")
class SignInOAuth42View(View):
    sign_in_oauth42_controller: BaseOAuth42Controller = None

    def __init__(self, sign_in_oauth42_controller: BaseOAuth42Controller) -> None:
        self.sign_in_oauth42_controller = sign_in_oauth42_controller

    async def get(self, request: HttpRequest) -> JsonResponse:
        data = await self.sign_in_oauth42_controller.handle_callback(request)
        data_json = json.loads(data.content)
        token = data_json["data"]["token"]
        is_temporary = data_json["data"]["is_temporary_token"]
        email = data_json["data"]["email"]
        frontend_url = OAuthUrls.FRONTEND_URL
        if is_temporary:
            frontend_url += f"?email={email}#two-factor-auth"
        #TODO - VERIFICAR SE É O PRIMEIRO LOGIN PARA REDIRECIONAR PARA A ROTA TEMPORARIA NO FRONT PARA NOTIFICAR OS OUTROS MS
        is_first_login = True
        if is_first_login:
            frontend_url = OAuthUrls.FRONTEND_URL_TEMP
        response = redirect(frontend_url)
        response.set_cookie("transcendence-auth_token", token)
        return response
