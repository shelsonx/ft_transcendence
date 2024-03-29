from ...models.two_factor import TwoFactor
from abc import ABC, abstractmethod


class ITwoFactorRepository(ABC):

    @abstractmethod
    async def add_two_factor(self, two_factor: TwoFactor) -> TwoFactor:
        pass

    @abstractmethod
    async def delete_two_factor(self, id: str) -> bool:
        pass

    @abstractmethod
    async def find_two_factor_by_user_id(self, user_id: str) -> TwoFactor:
        pass

    @abstractmethod
    async def delete_two_factor_by_user_id(self, user_id: str) -> bool:
        pass
