
from ..interfaces.controllers.base_controller import BaseController
from django.http import HttpRequest, JsonResponse
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.sign_in_oauth42_dto import SignInOAuth42Dto, SignInOAuth42DtoForm

class SignInOAuth42Controller(BaseController):

  def __init__(self, signin_oauth42_usecase: BaseUseCase) -> None:
    super().__init__()
    self.signin_oauth42_usecase = signin_oauth42_usecase

  def convert_to_form(self, request: HttpRequest) -> dict:
    return SignInOAuth42DtoForm(request.POST)

  def convert_to_dto(self, data: dict) -> SignInOAuth42Dto:
    return SignInOAuth42Dto(email=data.get('email'), password=data.get('password'))

  async def execute_post(self, dto: SignInOAuth42Dto) -> JsonResponse:
   return await self.signin_oauth42_usecase.execute(dto)