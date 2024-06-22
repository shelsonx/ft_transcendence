from abc import ABCMeta

from django.http import HttpRequest, JsonResponse
from django.http.request import HttpHeaders
import json

from ...exception.base_api_exception import BaseApiException

from ...entities.api_data_response import ApiDataResponse

from ...utils.to_json_response import to_json_response

from ...utils.http_response_to_json import http_response_to_json
from ...utils.get_prop_from_json import get_prop_from_json, get_data_from_json_response
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
      Route("/game-2factor-code/", ['POST', 'PUT'], handler_function=self.game_2factor_validate),
    ]
    super().__init__(http_client, routes_auth)
    self.register_functions = [self.register_game_info_ms, self.register_user_management_ms, self.register_game_ms]
    self.unregister_functions = [self.unregister_game_info_ms, self.unregister_user_management_ms, self.unregister_game_ms]
    self.rollback_register = False
    self.me_data = None

  def get_me(self, headers_dict: dict):
    http_client_data_user_me = HttpClientData(
      url="/user/",
      data={},
      headers=headers_dict
    )
    auth_data = self.http_client.get(http_client_data_user_me)
    data_json = self.convert_to_json_response(auth_data)
    return data_json

  def unregister_game_info_ms(self, auth_data_json, headers_dict):
    return self.notify_microservices("DELETE", ApiUrls.GAME_INFO, HttpClientData(
        url=f"/delete_user/",
        data=json.dumps({
            "id_msc": auth_data_json['id']
        }).encode('utf-8'),
        headers=headers_dict
    ))

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

  def unregister_game_ms(self, auth_data_json, headers_dict):
    return self.notify_microservices("DELETE", ApiUrls.GAME, HttpClientData(
        url=f"/user/{auth_data_json['id']}/",
        data={},
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


  def unregister_user_management_ms(self, auth_data_json, headers_dict):
    return self.notify_microservices("DELETE", ApiUrls.USER_MANAGEMENT, HttpClientData(
        url=f"/{auth_data_json['id']}/",
        data={},
        headers=headers_dict
    ))

  def register_user_management_ms(self, auth_data_json, headers_dict):
    body = json.dumps({
            "name": auth_data_json["user_name"],
            "user_uuid": auth_data_json['id'],
            "nickname": auth_data_json["user_name"],
            "email": auth_data_json['email'],
            "two_factor_enabled": auth_data_json['enable_2fa'],
            "avatar": "/media/avatars/default_avatar.jpeg",
            "chosen_language": "en"
        }).encode('utf-8')

    return self.notify_microservices("POST", ApiUrls.USER_MANAGEMENT, HttpClientData(
        url="",
        data=body,
        headers=headers_dict
    ))

  def register_ms(self, default_response, headers_dict):

        self.me_data = self.get_me(headers_dict)
        auth_data_json = json.loads(self.me_data.content)['data']

        if auth_data_json['enable_2fa']:
            return default_response

        if auth_data_json['is_first_login']:
            for index, register_function in enumerate(self.register_functions):
                response = register_function(auth_data_json, headers_dict)
                if response.status_code >= 400:
                    self.rollback_register = True
                    for i in range(index):
                        self.unregister_functions[i](auth_data_json, headers_dict)
                    return response
        return default_response

  def rollback_register_auth(self, headers_dict):
     if self.rollback_register:
            me = json.loads(self.me_data.content)['data']
            user_id = me['id']
            self.http_client.delete(HttpClientData(
                url=f"/user/{user_id}/",
                data={},
                headers=headers_dict
            ))

  def register_42(self, http_client_data: HttpClientData, request: HttpRequest, *args, **kwargs):
     try:
        data = ApiDataResponse(data={"message": "Ok"}, is_success=True, message="OK").to_dict()
        response = self.register_ms(JsonResponse(data=data, status=200, safe=False), request.headers)
        self.rollback_register_auth(request.headers)
        return response
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
        response = self.register_ms(sign_up_data_json, headers_dict)
        self.rollback_register_auth(headers_dict)
        return response
    except Exception as exception:
        return to_json_response(
            data=ApiDataResponse(message=str(exception), is_success=False), status=500
        )

  def get_blocked_users(self, user_id:str, headers:dict):
     data = self.notify_microservices("GET", ApiUrls.USER_MANAGEMENT, HttpClientData(
        url=f"/{user_id}/block/",
        data={},
        headers=headers
     ))
     data_json = get_data_from_json_response(data)
     if data.status_code >= 400:
        raise BaseApiException(
           message=f"{data_json.get('message')}-{user_id}",
           status_code=data.status_code
        )

     blocked_users = data_json.get('blocked_users')
     return blocked_users

  def game_2factor_validate(self, http_client_data: HttpClientData, request: HttpRequest, *args, **kwargs):
      try:
          if request.method == "PUT":
              response = self.http_client.put(http_client_data)
              return self.convert_to_json_response(response)

          decoded_data = http_client_data.data.decode('utf-8')
          data_dict = json.loads(decoded_data)

          user_receiver_ids = data_dict.get('user_receiver_ids')
          user_requester_id = data_dict.get('user_requester_id')

          user_receiver_ids_after_blocked = []
          for user_receiver_id in user_receiver_ids:
              blocked_users = self.get_blocked_users(user_receiver_id, http_client_data.headers)
              blocked_users_ids = [blocked_user['user_uuid'] for blocked_user in blocked_users]
              if user_requester_id not in blocked_users_ids:
                  user_receiver_ids_after_blocked.append(user_receiver_id)

          if len(user_receiver_ids_after_blocked) == 0:
                return to_json_response(
                    data=ApiDataResponse(
                         data={
                         "user_receiver_ids":[]
                    }, is_success=False),
                    status=404
                    )

          http_client_data.data = json.dumps({
             	"user_receiver_ids": user_receiver_ids_after_blocked,
                "user_requester_id": user_requester_id,
                "game_type": data_dict['game_type'],
                "game_id": data_dict['game_id']
          }).encode('utf-8')

          response = self.http_client.post(http_client_data)
          if response.status_code >= 400:
              return self.convert_to_json_response(response)
          return to_json_response(
              data=ApiDataResponse(
                 data={
                 "user_receiver_ids":user_receiver_ids_after_blocked
              }, is_success=True),
              status=200
            )
      except BaseApiException as exception:
            return to_json_response(
                data=ApiDataResponse(message=exception.message, is_success=False), status=exception.status_code
            )

      except Exception as exception:
          return to_json_response(
              data=ApiDataResponse(message=str(exception), is_success=False), status=500
          )
