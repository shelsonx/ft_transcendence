from ...dtos.validate_game_2factor_code_dto import ValidateGame2FactorCodeDto
from ...models.two_factor_game import TwoFactorGame
from abc import ABC, abstractmethod

class ITwoFactorGameRepository(ABC):

    @abstractmethod
    async def add_two_factor(self, two_factor: TwoFactorGame) -> TwoFactorGame:
        pass

    @abstractmethod
    async def delete_two_factor(self, id: str) -> bool:
        pass

    @abstractmethod
    async def find_two_factor_by_game_details(self, two_factor_game_dto: ValidateGame2FactorCodeDto) -> TwoFactorGame:
        pass

    @abstractmethod
    async def delete_two_factor_by_game_details(self, two_factor_game_dto: ValidateGame2FactorCodeDto) -> bool:
        pass
