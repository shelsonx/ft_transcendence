from ..interfaces.usecase.base_usecase import BaseUseCase
from ..exceptions.user_not_found_exception import UserNotFoundException
from ..dtos.validate_2factor_code_dto import Validate2FactorCodeDto
from ..interfaces.repositories.user_repository import IUserRepository
from ..services.two_factor_service import ITwoFactorService
from ..interfaces.repositories.two_factor_repository import ITwoFactorRepository
from django.core.exceptions import ObjectDoesNotExist
from ..interfaces.usecase.base_sign_in_usecase import BaseSignInUseCase


class Send2FactorCodeUseCase(BaseUseCase):
    def __init__(
        self, user_repository: IUserRepository, base_sign_in_use_case: BaseSignInUseCase
    ):
        self.user_repository = user_repository
        self.base_sign_in_use_case = base_sign_in_use_case

    async def execute(self, two_factor_dto: Validate2FactorCodeDto):
        user = None
        try:
            user = await self.user_repository.get_user_by_email(two_factor_dto.email)
        except ObjectDoesNotExist:
            raise UserNotFoundException()

        result = await self.base_sign_in_use_case.execute(
            user=user, is_temporary_token=True, expires_in_hours=2
        )
        return result.to_dict()
