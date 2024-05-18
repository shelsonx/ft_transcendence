from abc import ABCMeta

from django.http import HttpRequest
from django.http.request import HttpHeaders
import json

from ...utils.http_response_to_json import http_response_to_json
from ...utils.get_prop_from_json import get_prop_from_json
from ...utils.convert_to_json_response import convert_to_json_response
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

  def get_me(self, headers_dict: dict):
    http_client_data_user_me = HttpClientData(
      url="/user/",
      data={},
      headers=headers_dict
    )
    auth_data = self.http_client.get(http_client_data_user_me)
    data_json = http_response_to_json(auth_data)
    return data_json

  def register(self, http_client_data: HttpClientData, request: HttpRequest, *args, **kwargs):
    if request.method == "POST":
        return self.http_client.post(http_client_data)

    sign_in_dto = self.http_client.put(http_client_data)
    sign_in_dto_json = convert_to_json_response(sign_in_dto)
    sign_in_dto_data = get_prop_from_json(sign_in_dto_json)

    headers_dict = self.clone_header_with_auth(http_client_data.headers, sign_in_dto_data['token'])

    auth_me_data = self.get_me(headers_dict)

    print(auth_me_data)
    if auth_me_data['enable_2fa']:
        return sign_in_dto_data

    self.notify_microservices("POST", ApiUrls.GAME_INFO, HttpClientData(
        url="/register_user/",
        data=json.dumps({
            "id_msc": auth_me_data['id'],
            "full_name": auth_me_data["user_name"],
            "nickname": auth_me_data["user_name"]
        }).encode('utf-8'),
        headers=headers_dict
    ))
    '''
        {'id': '2f0b18d7-35b2-43c3-8091-7983356348c9', 'user_name': 'Bruno123', 'email': 'brunobonaldi94@gmail.com', 'login_type': {'name': 'email'}, 'enable_2fa': False, 'created_at': '2024-05-17T02:06:05.832Z', 'updated_at': '2024-05-17T02:06:05.832Z', 'is_active': True}
        if enable_2fa is True:
            nao enviar para os microservicos
        else:
            enviar para outros microservicos (quer dizer que o usuario esta se cadastrando)
    '''
    ######
    return sign_in_dto_data
