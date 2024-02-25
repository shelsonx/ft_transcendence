
from ..interfaces.services import TokenService
from ..models.user import User

class JWTService(TokenService):

  def __init__(self) -> None:
    pass

  def create_token(self, user: User) -> str:
    pass
  
  def verify_token(self, token: str) -> User:
    pass