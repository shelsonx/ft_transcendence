from ..interfaces.repositories.user_repository import IUserRepository
from ..interfaces.repositories.login_type_repository import ILoginTypeRepository
from ..interfaces.services import ITokenService
from ..constants.login_type_constants import LoginTypeConstants
from ..exceptions import FieldAlreadyExistsException, InvalidPasswordException
from ..models.user import User
from ..dtos.sign_up_dto import SignUpDto
from django.core.exceptions import ObjectDoesNotExist
from ..validators.password_validator import PasswordValidator
class SignUpUseCase:

    def __init__(self, user_repository: IUserRepository, token_service: ITokenService, login_type_repository: ILoginTypeRepository):
        self.user_repository = user_repository
        self.token_service = token_service
        self.login_type_repository = login_type_repository

    async def execute(self, sign_up_dto: SignUpDto):
        try:
            user = await self.user_repository.get_user_by_email_or_username(email=sign_up_dto.email, username=sign_up_dto.user_name)
            if user is not None:
                duplicated_field = "email" if user.email == sign_up_dto.email else "user_name"
                raise FieldAlreadyExistsException(duplicated_field)
        except ObjectDoesNotExist:    
        
            login_type = await self.login_type_repository.get_login_type_by_name(LoginTypeConstants.AUTH_EMAIL)
            password_validator = PasswordValidator()
            password_validator.validate(password=sign_up_dto.password)
            new_user = User(user_name=sign_up_dto.user_name, email=sign_up_dto.email, password=sign_up_dto.password, login_type=login_type)

            user = await self.user_repository.create_user(new_user)
            token = self.token_service.create_token(user)

            return token
            
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

from ..interfaces.usecase.base_sign_up_usecase import BaseSignUpUseCase
from ..interfaces.usecase.base_sign_in_usecase import BaseSignInUseCase


class SignUpUseCase(BaseSignUpUseCase):

    def __init__(
        self,
        user_repository: IUserRepository,
        login_type_repository: ILoginTypeRepository,
        two_factor_service: ITwoFactorService,
        base_sign_in_use_case: BaseSignInUseCase,
    ):
        self.two_factor_service = two_factor_service
        self.base_sign_in_use_case = base_sign_in_use_case
        super().__init__(user_repository, login_type_repository)

    async def execute(self, sign_up_dto: SignUpDto):
        try:
            await self.user_repository.get_user_by_email(email=sign_up_dto.email)
            raise FieldAlreadyExistsException("email")
        except ObjectDoesNotExist:
            base_sign_up_dto = BaseSignUpDto(
                email=sign_up_dto.email, user_name=sign_up_dto.user_name
            )
            new_user = await super().execute(
                sign_up_dto=base_sign_up_dto,
                password=sign_up_dto.password,
                login_type=LoginTypeConstants.AUTH_EMAIL,
            )
            result = await self.base_sign_in_use_case.execute(
                user=new_user, is_temporary_token=True
            )
            return result.to_dict()
