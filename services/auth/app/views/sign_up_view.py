from typing import Any
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views import View
from ..interfaces.controllers.base_controller import BaseController
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(View):
    sign_up_controller: BaseController = None

    def __init__(self, sign_up_controller: BaseController) -> None:
       self.sign_up_controller = sign_up_controller
       
    async def post(self, request: HttpRequest) -> JsonResponse:
        data = await self.sign_up_controller.handle_post(request)
        return data
