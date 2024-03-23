from abc import ABC, abstractmethod

class ITwoFactorService(ABC):

  @abstractmethod
  async def add_two_factor(self, user_id: str) -> None:
    pass

  @abstractmethod
  def generate_code(self) -> str:
    pass

  @abstractmethod
  def notify_user(self, user_id: str, code: str) -> None:
    pass

  @abstractmethod
  async def delete_two_factor(self, user_id: str) -> None:
    pass