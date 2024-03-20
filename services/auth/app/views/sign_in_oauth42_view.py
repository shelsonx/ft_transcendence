import json
from typing import Any
from django.http import HttpResponse, HttpRequest,JsonResponse
from django.views import View

from ..interfaces.services.http_client import IHttpClient
from ..interfaces.controllers.base_controller import BaseController
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..dtos.access_token_42 import AccessToken42
import os
from ..interfaces.usecase.base_usecase import BaseUseCase
@method_decorator(csrf_exempt, name='dispatch')

class SignInOAuth42View(View):
    sign_in_oauth42_controller: BaseController = None
    http_client: IHttpClient = None
    get_access_token_42_use_case: BaseUseCase = None
    validate_access_token_42_use_case: BaseUseCase = None
    get_me_42_use_case: BaseUseCase = None

    def __init__(self, sign_in_oauth42_controller: BaseController, http_client: IHttpClient, get_access_token_42_use_case: BaseUseCase, validate_access_token_42_use_case: BaseUseCase, get_me_42_use_case: BaseUseCase) -> None:
        self.sign_in_oauth42_controller = sign_in_oauth42_controller
        self.http_client = http_client
        self.get_access_token_42_use_case = get_access_token_42_use_case
        self.validate_access_token_42_use_case = validate_access_token_42_use_case
        self.get_me_42_use_case = get_me_42_use_case
       
    async def get(self, request: HttpRequest) -> JsonResponse:
        code = request.GET.get('code')
        response_data = await self.get_access_token_42_use_case.execute(code)
        
        access_token = response_data.access_token
        await self.validate_access_token_42_use_case.execute(access_token)

        me_data = await self.get_me_42_use_case.execute(access_token)
        return JsonResponse(data=me_data, status=200, safe=False)
