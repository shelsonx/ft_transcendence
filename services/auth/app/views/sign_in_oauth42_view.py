from typing import Any
from django.http import HttpResponse, HttpRequest,JsonResponse
from django.views import View

from ..utils.build_oauth42_url import build_oauth42_url
from ..interfaces.controllers.base_controller import BaseController
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import os
import urllib.parse
from ..constants.env_variables import EnvVariables
import http.client, urllib.parse
from django.shortcuts import redirect

@method_decorator(csrf_exempt, name='dispatch')
class SignInOAuth42View(View):
    sign_in_oauth42_controller: BaseController = None

    def __init__(self, sign_in_oauth42_controller: BaseController) -> None:
       self.sign_in_oauth42_controller = sign_in_oauth42_controller
       
    async def post(self, request: HttpRequest) -> JsonResponse:
        url_42 = build_oauth42_url()
        return redirect(url_42)
