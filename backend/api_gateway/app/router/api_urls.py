
class ApiUrl:

  def __init__(self, http_https, localhost_port, container_name_port, path) -> None:
    self.http_https = http_https
    self.path = path
    self.localhost_port = localhost_port
    self.container_name_port = container_name_port
    self.localhost = f"{http_https}://{localhost_port}/{path}"
    #"http://auth-api:80/api/auth/",
    self.container = f"{http_https}://{container_name_port}/{path}"
    #"http://localhost:8002/api/auth/"


  def rebuild_url(self, path: str, language: str = None):
    path_with_lang = f"{language}/{path}" if language else path

    self.localhost = f"{self.http_https}://{self.localhost_port}/{path_with_lang}"
    #"http://auth-api:80/api/auth/",
    self.container = f"{self.http_https}://{self.container_name_port}/{path_with_lang}"
    #"http://localhost:8002/api/auth/"

class ApiUrls:
  AUTH = ApiUrl("https", "localhost:8002", "auth-api:80", "api/auth/")
  USER_MANAGEMENT = ApiUrl("https", "localhost:8006", "user-management-api:8000", "user/")
  GAME_INFO = ApiUrl("https", "localhost:8003", "game-info:80", "dash/")
  GAME = ApiUrl("https", "localhost:8020", "game-api:8000", "")
