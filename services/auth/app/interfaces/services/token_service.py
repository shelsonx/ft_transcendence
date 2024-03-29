from abc import ABC, abstractmethod
from ...models.user import User


class ITokenService(ABC):

    @abstractmethod
    def create_token(self, user: User, expires_in_hours: int) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> User:
        pass
