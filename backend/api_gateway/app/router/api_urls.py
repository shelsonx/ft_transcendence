from dataclasses import dataclass

class ApiUrl:
  
  def __init__(self, http_https, localhost_port, container_name_port, path) -> None:
    self.http_https = http_https
    self.localhost = f"{http_https}://{localhost_port}/{path}"
    #"http://auth-api:80/api/auth/",
    self.container = f"{http_https}://{container_name_port}/{path}"
    #"http://localhost:8002/api/auth/"
  
  container: str
  localhost: str

class ApiUrls:
  AUTH = ApiUrl("http", "localhost:8002", "auth-api:80", "api/auth/")