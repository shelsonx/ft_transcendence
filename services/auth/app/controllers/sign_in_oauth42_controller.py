
from ..interfaces.controllers.base_controller import BaseController
from django.http import HttpRequest, JsonResponse
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.sign_in_oauth42_dto import SignInOAuth42Dto, SignInOAuth42DtoForm

class SignInOAuth42Controller():

  def __init__(self, signin_oauth42_usecase: BaseUseCase) -> None:
    self.signin_oauth42_usecase = signin_oauth42_usecase

  async def execute_get(self, dto: SignInOAuth42Dto) -> JsonResponse:
   return await self.signin_oauth42_usecase.execute(dto)