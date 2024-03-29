from ..exceptions.two_factor_exception import TwoFactorCodeException
from ..interfaces.services.two_factor_service import ITwoFactorService
from ..exceptions.user_inactive_exception import UserInactiveException
from ..interfaces.repositories.user_repository import IUserRepository
from ..interfaces.repositories.login_type_repository import ILoginTypeRepository
from ..interfaces.services import ITokenService
from ..constants.login_type_constants import LoginTypeConstants
from ..exceptions import FieldAlreadyExistsException
from ..dtos.sign_up_dto import SignUpDto
from ..dtos.two_factor_dto import TwoFactorDto
from ..interfaces.dtos.base_sign_up_dto import BaseSignUpDto
from django.core.exceptions import ObjectDoesNotExist
from ..utils.call_async import call_async

from ..interfaces.usecase.base_signup_usecase import BaseSignUpUseCase


class SignUpUseCase(BaseSignUpUseCase):

    def __init__(
        self,
        user_repository: IUserRepository,
        token_service: ITokenService,
        login_type_repository: ILoginTypeRepository,
        two_factor_service: ITwoFactorService,
    ):
        self.token_service = token_service
        self.two_factor_service = two_factor_service
        super().__init__(user_repository, login_type_repository)

    async def execute(self, sign_up_dto: SignUpDto):
        try:
            user = await self.user_repository.get_user_by_email(email=sign_up_dto.email)

            if user.is_active == True:
                raise FieldAlreadyExistsException("email")

            if user.is_active == False and sign_up_dto.two_factor_code is None:
                raise UserInactiveException()

            code_is_valid = (
                await self.two_factor_service.validate_and_delete_two_factor(
                    user_id=user.id, code=sign_up_dto.two_factor_code
                )
            )

            if code_is_valid == False:
                raise TwoFactorCodeException("Two factor code is invalid")

            user.is_active = True
            update_user = await self.user_repository.update_user(user)

            token = self.token_service.create_token(update_user)
            return token

        except ObjectDoesNotExist:
            base_sign_up_dto = BaseSignUpDto(
                email=sign_up_dto.email, user_name=sign_up_dto.user_name
            )
            new_user = await super().execute(
                sign_up_dto=base_sign_up_dto,
                password=sign_up_dto.password,
                login_type=LoginTypeConstants.AUTH_EMAIL,
            )
            await self.two_factor_service.send_code_to_user(
                new_user.id, email=new_user.email
            )
            return "Two factor code sent to email"
