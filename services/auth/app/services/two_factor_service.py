from ..interfaces.services.two_factor_service import ITwoFactorService
from ..interfaces.repositories.two_factor_repository import ITwoFactorRepository

class TwoFactorService(ITwoFactorService):

  def __init__(self, two_factor_repository: ITwoFactorRepository):
    self.two_factor_repository = two_factor_repository

  async def add_two_factor(self, user_id: str):
    pass

  def generate_code(self) -> str:
    pass

  def notify_user(self, user_id: str, code: str) -> None:
    pass

  async def delete_two_factor(self, user_id: str):
    pass

  async def validate_code(self, user_id: str, code: str) -> bool:
    pass