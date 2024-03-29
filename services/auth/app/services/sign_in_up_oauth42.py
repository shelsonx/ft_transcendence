from ..constants.login_type_constants import LoginTypeConstants
from ..models.user import User
from ..interfaces.repositories.user_repository import IUserRepository
from ..interfaces.services.token_service import ITokenService
from django.core.exceptions import ObjectDoesNotExist
from ..exceptions import InvalidPasswordException, UserNotFoundException
from ..dtos.sign_in_oauth42_dto import SignInUpOAuth42Dto
from datetime import datetime
from ..exceptions.token_expired_exception import TokenExpiredException
from ..interfaces.services.base_service import BaseService
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..interfaces.dtos.base_sign_up_dto import BaseSignUpDto
from ..exceptions import FieldAlreadyExistsException, InvalidPasswordException
from asgiref.sync import sync_to_async


class SignInOAuth42Service(BaseService):

    def __init__(
        self,
        user_repository: IUserRepository,
        token_service: ITokenService,
        base_sign_up_usecase: BaseUseCase,
    ):
        self.user_repository = user_repository
        self.token_service = token_service
        self.base_sign_up_usecase = base_sign_up_usecase

    async def execute(self, sign_in_up_OAuth42_dto: SignInUpOAuth42Dto):
        try:
            if not sign_in_up_OAuth42_dto.is_valid():
                raise TokenExpiredException()
            token_user = await self.user_repository.get_user_by_email(
                email=sign_in_up_OAuth42_dto.email
            )

            login_type = await sync_to_async(lambda: token_user.login_type)()
            if login_type.name != LoginTypeConstants.AUTH_42:
                raise FieldAlreadyExistsException("email")

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

        hours_to_expire = sign_in_up_OAuth42_dto.expire_to_hours()
        token = self.token_service.create_token(token_user, hours_to_expire)
        return token
