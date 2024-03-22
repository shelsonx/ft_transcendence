
from ..interfaces.controllers.base_oauth42_controller import BaseOAuth42Controller
from ..entities.api_data_response import ApiDataResponse
from ..interfaces.controllers.base_controller import BaseController
from django.http import HttpRequest, JsonResponse
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.sign_in_oauth42_dto import SignInUpOAuth42Dto, SignInOAuth42DtoForm
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..interfaces.services.http_client import IHttpClient
from ..interfaces.services.base_service import BaseService
from ..utils.to_json_response import to_json_response

class SignInOAuth42Controller(BaseOAuth42Controller):

  def __init__(self, http_client: IHttpClient, get_access_token_42_use_case: BaseUseCase, validate_access_token_42_use_case: BaseUseCase, get_me_42_use_case: BaseUseCase, sign_in_oauth42_service: BaseService) -> None:
    self.http_client = http_client
    self.get_access_token_42_use_case = get_access_token_42_use_case
    self.validate_access_token_42_use_case = validate_access_token_42_use_case
    self.get_me_42_use_case = get_me_42_use_case
    self.sign_in_oauth42_service = sign_in_oauth42_service

  async def handle_callback(self, request: HttpRequest) -> JsonResponse:
    code = request.GET.get('code')
    response_data = await self.get_access_token_42_use_case.execute(code)
    
    access_token = response_data.access_token
    await self.validate_access_token_42_use_case.execute(access_token)

    me_data = await self.get_me_42_use_case.execute(access_token)
    sign_in_up_oath42 = SignInUpOAuth42Dto(email=me_data['email'], user_name=me_data['login'], access_token=access_token, expires_in=response_data.expires_in)
    data = await self.sign_in_oauth42_service.execute(sign_in_up_oath42)
    return to_json_response(ApiDataResponse(data=data))
