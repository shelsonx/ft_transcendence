from abc import ABC, abstractmethod
from ...models.user import User

class ITokenService(ABC):

    @abstractmethod
    def create_token(self, user: User) -> str:
        pass
    @abstractmethod
    def verify_token(self, token: str) -> User:
        pass
from abc import ABC, abstractmethod
from ...models.user import User


class ITokenService(ABC):

    @abstractmethod
    def create_token(
        self, user: User, expires_in_hours: int, secret: str = None
    ) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str, secret: str = None) -> User:
        pass
