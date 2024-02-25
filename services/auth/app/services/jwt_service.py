
from ..interfaces.services.token_service import ITokenService
from ..models.user import User

class JWTService(ITokenService):

  def __init__(self) -> None:
    pass

  def create_token(self, user: User) -> str:
    return "token"
  
  def verify_token(self, token: str) -> User:
    return User()