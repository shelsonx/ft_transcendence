


from ..interfaces.controllers.base_controller import BaseController
from django.http import HttpRequest
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.sign_up_dto import SignUpDto
from ..dtos.sign_up_dto import SignUpDtoForm, SignUpDto

class SignUpController(BaseController):

  def __init__(self, sign_up_usecase: BaseUseCase) -> None:
    super().__init__()                     
    self.sign_up_usecase = sign_up_usecase

  def convert_to_form(self, request: HttpRequest) -> dict:
    return SignUpDtoForm(request.POST)
  
  def convert_to_dto(self, data: dict) -> SignUpDto:
    return SignUpDto(email=data.get('email'), password=data.get('password'), user_name=data.get('user_name'))

  async def execute(self, dto: SignUpDto):
    return await self.sign_up_usecase.execute(dto)