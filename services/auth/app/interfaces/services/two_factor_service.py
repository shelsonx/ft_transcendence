from abc import ABC, abstractmethod
from ...dtos.two_factor_dto import TwoFactorDto

class ITwoFactorService(ABC):

  @abstractmethod
  async def add_two_factor(self, user_id: str) -> None:
    pass

  @abstractmethod
  def generate_code(self) -> str:
    pass

  @abstractmethod
  async def validate_code(self, two_factor_dto: TwoFactorDto) -> bool:
    pass

  @abstractmethod
  def notify_user(self, two_factor_dto: TwoFactorDto) -> None:
    pass

  @abstractmethod
  async def delete_two_factor(self, user_id: str) -> None:
    pass