from ..interfaces.usecase.base_usecase import BaseUseCase
from ..exceptions.user_not_found_exception import UserNotFoundException
from ..dtos.validate_2factor_code_dto import Validate2FactorCodeDto
from ..interfaces.repositories.user_repository import IUserRepository
from ..services.two_factor_service import ITwoFactorService
from ..interfaces.repositories.two_factor_repository import ITwoFactorRepository
from django.core.exceptions import ObjectDoesNotExist


class Send2FactorCodeUseCase(BaseUseCase):
    def __init__(
        self, user_repository: IUserRepository, two_factor_service: ITwoFactorService
    ):
        self.two_factor_service = two_factor_service
        self.user_repository = user_repository

    async def execute(self, two_factor_dto: Validate2FactorCodeDto):
        user = None
        try:
            user = await self.user_repository.get_user_by_email(two_factor_dto.email)
        except ObjectDoesNotExist:
            raise UserNotFoundException()

        await self.two_factor_service.send_code_to_user(user.id, email=user.email)
