


from ..interfaces.controllers.base_controller import BaseController
from django.http import HttpRequest, HttpResponse
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.sign_up_dto import SignUpDto
from typing import Dict
from ..entities.fields import Field
from django.core.validators import validate_email
class SignUpController(BaseController):

  def __init__(self, sign_up_usecase: BaseUseCase) -> None:
    super().__init__(
      fields={
        "email":Field(name='email', is_required=True, field_type=str, validators=[validate_email]),
        "password":Field(name='password', is_required=True, field_type=str),
        "user_name": Field(name='user_name', is_required=True, field_type=str),
      }
    )                     
    self.sign_up_usecase = sign_up_usecase
    self.dto: SignUpDto = None

  def convert_to_dto(self, data: dict) -> SignUpDto:
    return SignUpDto(email=data.get('email'), password=data.get('password'), user_name=data.get('user_name'))

  async def execute(self, dto: SignUpDto) -> HttpResponse:
    return await self.sign_up_usecase.execute(dto)