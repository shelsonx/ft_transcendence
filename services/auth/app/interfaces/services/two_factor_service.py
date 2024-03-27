from abc import ABC, abstractmethod

from ..repositories.two_factor_repository import ITwoFactorRepository

from ...models.two_factor import TwoFactor
from ...dtos.two_factor_dto import TwoFactorDto

class ITwoFactorService(ABC):

  def __init__(self, two_factor_repository: ITwoFactorRepository):
    self.two_factor_repository = two_factor_repository

  async def add_two_factor(self, user_id: str):
    two_factor = TwoFactor(code=self.generate_code(), user_id=user_id)
    return await self.two_factor_repository.add_two_factor(two_factor)

  @abstractmethod
  def generate_code(self) -> str:
    pass

  @abstractmethod
  async def validate_code(self, user_id: str, code: str) -> bool:
    pass

  @abstractmethod
  def notify_user(self, email: str, code: str) -> None:
    pass

  async def delete_two_factor(self, user_id: str) -> None:
    await self.two_factor_repository.delete_two_factor_by_user_id(user_id)