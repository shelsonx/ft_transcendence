from ...models.login_type import LoginType
from abc import ABC, abstractmethod
class ILoginTypeRepository(ABC):

  @abstractmethod
  async def get_login_type_by_name(self, name: str) -> LoginType:
    pass