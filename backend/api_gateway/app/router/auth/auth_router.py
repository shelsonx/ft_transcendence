from abc import ABCMeta

from django.http import HttpRequest, JsonResponse
from django.http.request import HttpHeaders
import json

from ...entities.api_data_response import ApiDataResponse

from ...utils.to_json_response import to_json_response

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
      Route("/register-42/", ['GET'], handler_function=self.register_42),
    ]
    super().__init__(http_client, routes_auth)

  def get_me(self, headers_dict: dict):
    http_client_data_user_me = HttpClientData(
      url="/user/",
      data={},
      headers=headers_dict
    )
    auth_data = self.http_client.get(http_client_data_user_me)
    data_json = self.convert_to_json_response(auth_data)
    return data_json

  def register_game_info_ms(self, auth_data_json, headers_dict):
    body = json.dumps({
                    "id_msc": auth_data_json['id'],
                    "full_name": auth_data_json["user_name"],
                    "nickname": auth_data_json["user_name"]
                }).encode('utf-8')

    return self.notify_microservices("POST", ApiUrls.GAME_INFO, HttpClientData(
        url="/register_user/",
        data=body,
        headers=headers_dict
    ))

  def register_game_ms(self, auth_data_json, headers_dict):
     body = json.dumps({
            "id": auth_data_json['id'],
            "username": auth_data_json["user_name"],
        }).encode('utf-8')
     return self.notify_microservices("POST", ApiUrls.GAME, HttpClientData(
        url=f"/user/",
        data=body,
        headers=headers_dict
     ))

  def register_user_management_ms(self, auth_data_json, headers_dict):
    body = json.dumps({
            "name": auth_data_json["user_name"],
            "user_uuid": auth_data_json['id'],
            "nickname": auth_data_json["user_name"],
            "email": auth_data_json['email'],
            "two_factor_enabled": auth_data_json['enable_2fa'],
            "chosen_language": "en"
        }).encode('utf-8')

    return self.notify_microservices("POST", ApiUrls.USER_MANAGEMENT, HttpClientData(
        url="",
        data=body,
        headers=headers_dict
    ))

  def register_ms(self, default_response, headers_dict):

        auth_me_data = self.get_me(headers_dict)
        auth_data_json = json.loads(auth_me_data.content)['data']

        if auth_data_json['enable_2fa']:
            return default_response

        if auth_data_json['is_first_login']:
            game_info_data = self.register_game_info_ms(auth_data_json, headers_dict)
            print(game_info_data)
            user_management_data = self.register_user_management_ms(auth_data_json, headers_dict)
            print(user_management_data)
            game_data = self.register_game_ms(auth_data_json, headers_dict)
            print(game_data)
        return default_response

  def register_42(self, http_client_data: HttpClientData, request: HttpRequest, *args, **kwargs):
     try:
        data = ApiDataResponse(data={"message": "Ok"}, is_success=True, message="OK").to_dict()
        return self.register_ms(JsonResponse(data=data, status=200, safe=False), request.headers)
     except Exception as exception:
        return to_json_response(
            data=ApiDataResponse(message=str(exception), is_success=False), status=500
        )
  def register(self, http_client_data: HttpClientData, request: HttpRequest, *args, **kwargs):
    try:
        if request.method == "POST":
            response =  self.http_client.post(http_client_data)
            return self.convert_to_json_response(response)

        sign_up_data = self.http_client.put(http_client_data)
        sign_up_data_json = self.convert_to_json_response(sign_up_data)
        if sign_up_data.status_code >= 400:
            return sign_up_data_json

        headers_dict = self.clone_header_with_auth(http_client_data.headers, sign_up_data.json()['data']['token'])
        self.register_ms(sign_up_data_json, headers_dict)
        return sign_up_data_json
    except Exception as exception:
        return to_json_response(
            data=ApiDataResponse(message=str(exception), is_success=False), status=500
        )
