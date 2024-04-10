from ...interfaces.repositories.user_repository import IUserRepository
from ...interfaces.repositories.login_type_repository import ILoginTypeRepository
from ...interfaces.services import ITokenService
from ...constants.login_type_constants import LoginTypeConstants
from ...exceptions import FieldAlreadyExistsException, NotValidPasswordException
from ...models.user import User
from ...interfaces.dtos.base_sign_up_dto import BaseSignUpDto
from django.core.exceptions import ObjectDoesNotExist
from ...validators.password_validator import PasswordValidator
from ...interfaces.usecase.base_usecase import BaseUseCase
from ...interfaces.services.two_factor_service import ITwoFactorService
from ...dtos.sign_in_dto import SignInResultDto
from os import environ
from ...constants.env_variables import EnvVariables


class BaseSignInUseCase(BaseUseCase):

    def __init__(
        self,
        token_service: ITokenService,
        two_factor_service: ITwoFactorService,
    ):
        self.token_service = token_service
        self.two_factor_service = two_factor_service

    def _create_token(
        self, user: User, is_temporary_token: str, expires_in_hours: int = None
    ) -> str:
        if is_temporary_token:
            return self.token_service.create_token(
                user=user,
                expires_in_hours=expires_in_hours,
                secret=environ.get(EnvVariables.TEMPORARY_JWT_SECRET),
            )
        return self.token_service.create_token(user, expires_in_hours=expires_in_hours)

    async def _send_code_and_return_token(
        self, user: User, is_temporary_token: bool, expires_in_hours: int
    ) -> SignInResultDto:
        await self.two_factor_service.send_code_to_user(user.id, email=user.email)
        token = self._create_token(
            user,
            is_temporary_token=is_temporary_token,
            expires_in_hours=expires_in_hours,
        )
        return SignInResultDto(token=token, is_temporary_token=is_temporary_token)

    async def execute(
        self, user: User, is_temporary_token: bool, expires_in_hours: int = 2
    ) -> SignInResultDto:

        if is_temporary_token:
            return await self._send_code_and_return_token(
                user, is_temporary_token, expires_in_hours
            )
        token = self._create_token(
            user,
            is_temporary_token=is_temporary_token,
            expires_in_hours=expires_in_hours,
        )
        return SignInResultDto(token=token, is_temporary_token=is_temporary_token)
