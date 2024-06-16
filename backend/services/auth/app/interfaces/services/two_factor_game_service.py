from abc import ABC, abstractmethod
from datetime import timedelta
from typing import List
from ..repositories.two_factor_game_repository import ITwoFactorGameRepository
from ...exceptions.two_factor_exception import TwoFactorCodeException
from ...models.two_factor_game import TwoFactorGame
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from ...dtos.validate_game_2factor_code_dto import ValidateGame2FactorCodeDto, SendGame2FactorCodeDto
from ...models.user import User

class ITwoGameFactorService(ABC):

    def __init__(self, two_factor_game_repository: ITwoFactorGameRepository):
        self.two_factor_game_repository = two_factor_game_repository

    async def add_two_factor(self, user_receiver_id:str, user_requester_id: str, game_type: str,game_id: str) -> TwoFactorGame:
        two_factor = TwoFactorGame(
            code=self.generate_code(),
            user_receiver_id=user_receiver_id,
            user_requester_id=user_requester_id,
            game_type=game_type,
            game_id=game_id)
        return await self.two_factor_game_repository.add_two_factor(two_factor)

    @abstractmethod
    def generate_code(self) -> str:
        pass

    @abstractmethod
    async def validate_code(self, two_factor_code: ValidateGame2FactorCodeDto) -> bool:
        pass

    @abstractmethod
    def notify_user(self, email: str, code: str) -> None:
        pass

    async def send_code_to_user(self, two_factor_game: SendGame2FactorCodeDto, users: List[User]) -> None:
        try:

            ids = list(map(lambda user: user.id, users))
            for user_receiver_id in two_factor_game.user_receiver_ids:
                if user_receiver_id not in ids:
                    raise TwoFactorCodeException(_("Invalid email list"))

            two_factor_code = (
                await self.two_factor_game_repository.find_two_factor_by_game_details(two_factor_game)
            )
            print("two_factor_code",two_factor_code)
        except TwoFactorGame.DoesNotExist:
            pass
        if two_factor_code is not None:
            await self.two_factor_game_repository.delete_two_factor_by_ids(
                [two_factor.id for two_factor in two_factor_code]
            )

        user_requester = next(user for user in users if user.id == two_factor_game.user_requester_id)
        for user_receiver_id in two_factor_game.user_receiver_ids:
            user_receiver = next(user for user in users if user.id == user_receiver_id)
            two_factor_dto = await self.add_two_factor(
                user_receiver_id=user_receiver,
                user_requester_id=user_requester,
                game_type=two_factor_game.game_type,
                game_id=two_factor_game.game_id
            )
            self.notify_user(user_receiver.email, two_factor_dto.code)

    async def validate_and_delete_two_factor(self, two_factor_game_dto: ValidateGame2FactorCodeDto) -> bool:
       return await self.validate_code(two_factor_game_dto)
    async def delete_two_factor(self, user_id: str) -> None:
        await self.two_factor_game_repository.delete_two_factor_by_user_id(user_id)
