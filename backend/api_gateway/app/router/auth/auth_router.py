from ...services.http_client import IHttpClient
from ...interfaces.router.router import IRouter, Route

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