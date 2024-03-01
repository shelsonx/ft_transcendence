
from ..interfaces.controllers.base_controller import BaseController
from django.http import HttpRequest, JsonResponse
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.sign_in_dto import SignInDto, SignInDtoForm

class UserController(BaseController):

  def __init__(self, edit_user_usecase: BaseUseCase, delete_user_usecase) -> None:
    super().__init__()
    self.edit_user_usecase = edit_user_usecase
    self.delete_user_usecase = delete_user_usecase

  def convert_to_form(self, request: HttpRequest) -> dict:
    return SignInDtoForm(request.POST)

  def convert_to_dto(self, data: dict) -> SignInDto:
    return SignInDto(email=data.get('email'), password=data.get('password'))

  async def execute_put(self, user_id: str, dto: SignInDto) -> JsonResponse:
   return await self.edit_user_usecase.execute(user_id, dto)