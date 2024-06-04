from ..exceptions.user_not_found_exception import UserNotFoundException
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..dtos.forgot_password_dto import ForgotPasswordDto
from ..interfaces.repositories.user_repository import IUserRepository
from ..services.two_factor_service import ITwoFactorService
from django.core.exceptions import ObjectDoesNotExist
from ..exceptions.two_factor_exception import TwoFactorCodeException
from ..interfaces.usecase.base_sign_in_usecase import BaseSignInUseCase
from ..validators.password_validator import PasswordValidator
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _


class ForgotPasswordUseCase(BaseUseCase):
    def __init__(
        self,
        user_repository: IUserRepository,
        two_factor_service: ITwoFactorService,
        base_sign_in_usecase: BaseSignInUseCase,
    ):
        self.two_factor_service = two_factor_service
        self.user_repository = user_repository
        self.base_sign_in_usecase = base_sign_in_usecase

    async def execute(self, forgot_password_dto: ForgotPasswordDto):
        user = None
        try:
            user = await self.user_repository.get_user_by_email(
                forgot_password_dto.email
            )
        except ObjectDoesNotExist:
            raise UserNotFoundException()

        is_valid = await self.two_factor_service.validate_and_delete_two_factor(
            user.id, code=forgot_password_dto.two_factor_code
        )
        if not is_valid:
            invalid_code = _("Invalid two factor code")
            raise TwoFactorCodeException(invalid_code)

        password_validator = PasswordValidator()
        password_validator.validate(forgot_password_dto.password)
        user.password = make_password(forgot_password_dto.password)
        if not user.is_active:
            user.is_active = True
        updated_user = await self.user_repository.update_user(user)

        result = await self.base_sign_in_usecase.execute(
            user=updated_user,
            is_temporary_token=False,
        )
        return result.to_dict()
