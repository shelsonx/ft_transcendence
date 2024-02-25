from abc import ABC, abstractmethod
from ...models.user import User

class IAuthRepository(ABC):

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User:
        pass
    @abstractmethod
    async def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, id: str) -> User:
        pass

    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete_user(self, username: str) -> bool:
        pass