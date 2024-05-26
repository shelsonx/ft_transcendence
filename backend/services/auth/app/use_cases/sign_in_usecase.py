from ..interfaces.usecase.base_sign_in_usecase import BaseSignInUseCase
from ..models.user import User
from ..interfaces.services.two_factor_service import ITwoFactorService
from ..interfaces.repositories.user_repository import IUserRepository
from ..interfaces.services.token_service import ITokenService
from django.core.exceptions import ObjectDoesNotExist
from ..exceptions import InvalidPasswordException, UserNotFoundException
from ..dtos.sign_in_dto import SignInDto, SignInResultDto
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..exceptions.two_factor_exception import TwoFactorCodeException
from ..exceptions.forbidden_exception import ForbiddenException
from ..constants.login_type_constants import LoginTypeConstants
from asgiref.sync import sync_to_async
from ..constants.env_variables import EnvVariables
from os import environ


class SignInUseCase(BaseSignInUseCase):

    def __init__(
        self,
        user_repository: IUserRepository,
        token_service: ITokenService,
        two_factor_service: ITwoFactorService,
    ):
        super().__init__(token_service, two_factor_service)
        self.user_repository = user_repository

    async def get_login_type(self, user: User):
        return await sync_to_async(lambda: user.login_type)()

    async def execute(self, sign_in_dto: SignInDto) -> dict:
        try:
            user = await self.user_repository.get_user_by_email(email=sign_in_dto.email)

            login_type = await self.get_login_type(user)
            if login_type.name != LoginTypeConstants.AUTH_EMAIL:
                raise ForbiddenException("Forbidden access to this login type")

            should_send_temporary_token = not user.is_active or user.enable_2fa

            if should_send_temporary_token:
                result = await super().execute(user, should_send_temporary_token)
                return result.to_dict()

        except ObjectDoesNotExist:
            raise UserNotFoundException()

        if not user.check_password(sign_in_dto.password):
            raise InvalidPasswordException()

        result = await super().execute(user, False, True)
        return result.to_dict()
