from ..exceptions.user_not_found_exception import UserNotFoundException
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.validate_game_2factor_code_dto import ValidateGame2FactorCodeDto
from ..interfaces.repositories.user_repository import IUserRepository
from ..services.two_game_factor_service import TwoGameFactorService
from ..interfaces.repositories.two_factor_repository import ITwoFactorRepository
from django.core.exceptions import ObjectDoesNotExist
from ..exceptions.two_factor_exception import TwoFactorCodeException
from ..interfaces.usecase.base_sign_in_usecase import BaseSignInUseCase
from django.utils.translation import gettext_lazy as _


class ValidateGame2FactorCodeUseCase(BaseUseCase):
    def __init__(
        self,
        user_repository: IUserRepository,
        two_factor_service: TwoGameFactorService,
    ):
        self.two_factor_service = two_factor_service
        self.user_repository = user_repository

    async def execute(self, two_factor_dto: ValidateGame2FactorCodeDto):
        user = None
        try:
            ids = [two_factor_dto.user_requester_id] + list(dict(two_factor_dto.code_user_receiver_id).values())
            users = await self.user_repository.get_users_by_ids(ids)
            if len(users) != len(ids):
                raise UserNotFoundException()
        except ObjectDoesNotExist:
            raise UserNotFoundException()

        is_valid = await self.two_factor_service.validate_and_delete_two_factor(
            two_factor_dto
        )
        if not is_valid:
            invalid_code = _("Invalid two factor code")
            raise TwoFactorCodeException(invalid_code)
        result = {"message": "Two factor code validated successfully"}
        return result
