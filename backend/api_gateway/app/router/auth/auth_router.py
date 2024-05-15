from abc import ABCMeta

from django.http import HttpRequest

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
      Route("/validate-2factor-code/", ['POST', 'PUT']),
    ]
    super().__init__(http_client, routes_auth)

  def register(self, http_client_data: HttpClientData, request: HttpRequest, *args, **kwargs):
    auth_response = self.http_client.post(http_client_data)
    auth_data = convert_to_json_response(auth_response)
    print("auth_data", auth_data)
    http_client = HttpClient(ApiUrls.USER_MANAGEMENT)
    http_client_data_user_management = HttpClientData(
      url="",
      data={
        "user_uuid": auth_data["id"],
        "name": auth_data["user_name"],
        "nickname": auth_data["user_name"],
        "two_factor_enabled": auth_data["enable_2fa"],
        "email": auth_data["email"],
        "chosen_language": "en",
        "status": "active"
      },
      headers=http_client_data.headers
    )
    http_client.post(http_client_data_user_management)
    return auth_data
