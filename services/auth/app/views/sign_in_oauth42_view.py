import json
from typing import Any
from django.http import HttpResponse, HttpRequest,JsonResponse
from django.views import View

from ..interfaces.services.http_client import IHttpClient
from ..interfaces.controllers.base_controller import BaseController
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ..constants.env_variables import EnvVariables
import os
@method_decorator(csrf_exempt, name='dispatch')

class SignInOAuth42View(View):
    sign_in_oauth42_controller: BaseController = None
    http_client: IHttpClient = None

    def __init__(self, sign_in_oauth42_controller: BaseController, http_client: IHttpClient) -> None:
        self.sign_in_oauth42_controller = sign_in_oauth42_controller
        self.http_client = http_client
       
    async def get(self, request: HttpRequest) -> JsonResponse:
        client_id = os.environ.get(EnvVariables.OAUTH42_CLIENT_ID)
        secret_id = os.environ.get(EnvVariables.OAUTH42_SECRET_KEY)
        url_redirect = os.environ.get(EnvVariables.OAUTH42_REDIRECT_URI)
        code = request.GET.get('code')
        data = {
            'client_id': client_id,
            'client_secret': secret_id,
            'redirect_uri': url_redirect.rstrip('/'),
            'grant_type': 'authorization_code',
            'code': code
        }
        response = self.http_client.post('https://api.intra.42.fr/oauth/token', data=data, headers={"Content-type": "application/x-www-form-urlencoded"})
        response_data = self.http_client.serialize(response)
        me_response = self.http_client.get('https://api.intra.42.fr/v2/me', headers={"Authorization": f"Bearer {response_data['access_token']}"})
        me_data = self.http_client.serialize(me_response)
        return JsonResponse(data=me_data, status=200, safe=False)
