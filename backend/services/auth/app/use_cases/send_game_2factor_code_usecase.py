import asyncio

from ..exceptions.individual_game_exception import IndividualGameException
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..exceptions.user_not_found_exception import UserNotFoundException
from ..dtos.validate_game_2factor_code_dto import SendGame2FactorCodeDto
from ..repositories.two_game_factor_repository import ITwoFactorGameRepository
from ..interfaces.repositories.two_factor_repository import ITwoFactorRepository
from django.core.exceptions import ObjectDoesNotExist
from ..interfaces.usecase.base_sign_in_usecase import BaseSignInUseCase
from ..interfaces.services.two_factor_game_service import ITwoGameFactorService
from ..interfaces.repositories.user_repository import IUserRepository
from asgiref.sync import sync_to_async
from ..models.two_factor_game import TwoFactorGame
class Send2GameFactorCodeUseCase(BaseUseCase):
    def __init__(
        self,
        user_repository: IUserRepository,
        two_factor_service: ITwoGameFactorService
    ):
        self.user_repository = user_repository
        self.two_factor_service = two_factor_service

    async def execute(self, two_factor_dto: SendGame2FactorCodeDto):
        user = None
        try:
            ids = two_factor_dto.user_receiver_ids + [two_factor_dto.user_requester_id]
            if two_factor_dto.game_type == TwoFactorGame.GameType.INDIVIDUAL_GAME.value and len(two_factor_dto.user_receiver_ids) >= 2:
                raise IndividualGameException()
            user = await self.user_repository.get_users_by_ids(ids=ids)
            if len(user) != len(ids):
                raise UserNotFoundException()
        except ObjectDoesNotExist:
            raise UserNotFoundException()
        # user_without_requester = list(filter(lambda user: user.id != two_factor_dto.user_requester_id, user))
        await self.two_factor_service.send_code_to_user(
            two_factor_game=two_factor_dto, users=user
        )
        return {"message": "Code sent successfully"}

