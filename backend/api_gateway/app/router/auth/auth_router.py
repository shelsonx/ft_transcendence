from abc import ABCMeta

from django.http import HttpRequest
from django.http.request import HttpHeaders

from ...utils.convert_to_json_response import convert_to_json_response
from ...utils.get_prop_from_json import get_prop_from_json
from ...services.http_client import IHttpClient
from ...interfaces.router.router import IRouter, Route
from ...services.http_client import HttpClient
from ...interfaces.services.http_client import IHttpClient, HttpClientData
from ..api_urls import ApiUrls

class AuthRouter(IRouter):

  def __init__(self, http_client: IHttpClient) -> None:
    routes_auth = [
      Route("/forgot-password/", ['POST']),
      Route("/redirect-42/", ['GET'], True),
      Route("/sign-in/", ['POST']),
      Route("/sign-up/", ['POST']),
      Route("/user/", ['GET']),
      Route("/user/<uuid:user_id>", ['PUT', 'DELETE']),
      Route("/sign-in-42/", ['POST']),
      Route("/validate-2factor-code/", allowed_verbs=['POST', 'PUT'], handler_function=self.register),
    ]
    super().__init__(http_client, routes_auth)

  def register(self, http_client_data: HttpClientData, request: HttpRequest, *args, **kwargs):
    if request.method == "POST":
        return self.http_client.post(http_client_data)

    sign_in_dto = self.http_client.put(http_client_data)
    sign_in_dto_data = convert_to_json_response(sign_in_dto)
    data = get_prop_from_json(sign_in_dto_data)

    #http_client = HttpClient(ApiUrls.USER_MANAGEMENT)
    ##########GET USER DETAILS
    original_headers = http_client_data.headers
    headers_dict = {k: original_headers[k] for k in original_headers}
    headers_dict['Authorization'] = f"Bearer {data['token']}"

    http_client_data_user_me = HttpClientData(
      url="/user/",
      data={},
      headers=headers_dict
    )
    auth_data = self.http_client.get(http_client_data_user_me)
    auth_data_json = convert_to_json_response(auth_data)
    data_json = get_prop_from_json(auth_data_json)
    print(data_json)
    '''
        {'id': '2f0b18d7-35b2-43c3-8091-7983356348c9', 'user_name': 'Bruno123', 'email': 'brunobonaldi94@gmail.com', 'login_type': {'name': 'email'}, 'enable_2fa': False, 'created_at': '2024-05-17T02:06:05.832Z', 'updated_at': '2024-05-17T02:06:05.832Z', 'is_active': True}
        if enable_2fa is True:
            nao enviar para os microservicos
        else:
            enviar para outros microservicos (quer dizer que o usuario esta se cadastrando)
    '''
    ######
    return sign_in_dto_data
