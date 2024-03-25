


from ..entities.api_data_response import ApiDataResponse
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

  async def execute_post(self, dto: SignUpDto):
    return await self.sign_up_usecase.execute(dto)
  
  async def handle_post(self, request: HttpRequest):
    await super().handle_post(request)
    return self.to_json_response(data=ApiDataResponse(message="User created successfully. Validate code through email"), status=201)
