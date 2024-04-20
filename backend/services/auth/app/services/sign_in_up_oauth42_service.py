from ..models.user import User
from .two_factor_service import ITwoFactorService
from ..constants.login_type_constants import LoginTypeConstants
from ..interfaces.repositories.user_repository import IUserRepository
from ..interfaces.services.token_service import ITokenService
from ..dtos.sign_in_oauth42_dto import SignInUpOAuth42Dto
from ..dtos.sign_in_dto import SignInResultDto
from django.core.exceptions import ObjectDoesNotExist
from ..exceptions.token_expired_exception import TokenExpiredException
from ..exceptions import FieldAlreadyExistsException
from ..interfaces.services.base_service import BaseService
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..interfaces.dtos.base_sign_up_dto import BaseSignUpDto
from asgiref.sync import sync_to_async
from ..constants.env_variables import EnvVariables
from os import environ
from ..interfaces.usecase.base_sign_in_usecase import BaseSignInUseCase
from ..interfaces.usecase.base_sign_up_usecase import BaseSignUpUseCase


class SignInOAuth42Service(BaseService):

    def __init__(
        self,
        user_repository: IUserRepository,
        base_sign_up_usecase: BaseSignUpUseCase,
        base_sign_in_usecase: BaseSignInUseCase,
    ):
        self.user_repository = user_repository
        self.base_sign_up_usecase = base_sign_up_usecase
        self.base_sign_in_usecase = base_sign_in_usecase

    async def get_login_type(self, user: User):
        return await sync_to_async(lambda: user.login_type)()

    async def execute(
        self, sign_in_up_OAuth42_dto: SignInUpOAuth42Dto
    ) -> SignInResultDto:
        try:
            if not sign_in_up_OAuth42_dto.is_valid():
                raise TokenExpiredException()

            token_user = await self.user_repository.get_user_by_email(
                email=sign_in_up_OAuth42_dto.email
            )
            login_type = await self.get_login_type(token_user)
            if login_type.name != LoginTypeConstants.AUTH_42:
                raise FieldAlreadyExistsException("email")

            if token_user.enable_2fa:
                return await self.base_sign_in_usecase.execute(token_user, True)

        except ObjectDoesNotExist:
            base_signup_dto = BaseSignUpDto(
                email=sign_in_up_OAuth42_dto.email,
                user_name=sign_in_up_OAuth42_dto.user_name,
            )
            token_user = await self.base_sign_up_usecase.execute(
                sign_up_dto=base_signup_dto,
                password=None,
                login_type=LoginTypeConstants.AUTH_42,
                is_active=True,
            )

        token_user.is_active = True
        await self.user_repository.update_user(token_user)

        return await self.base_sign_in_usecase.execute(token_user, False)
