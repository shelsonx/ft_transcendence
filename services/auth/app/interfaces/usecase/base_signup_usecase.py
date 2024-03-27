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

class BaseSignUpUseCase(BaseUseCase):

    def __init__(self, user_repository: IUserRepository, login_type_repository: ILoginTypeRepository):
        self.user_repository = user_repository
        self.login_type_repository = login_type_repository

    async def execute(self, sign_up_dto: BaseSignUpDto, password: str = None, login_type: str = LoginTypeConstants.AUTH_EMAIL) -> User:
        
        if password is None and login_type == LoginTypeConstants.AUTH_EMAIL:
            raise NotValidPasswordException(message="Password is required for email sign up")
        login_type = await self.login_type_repository.get_login_type_by_name(login_type)
        
        if password is not None:
            password_validator = PasswordValidator()
            password_validator.validate(password=password)
        
        new_user = User(user_name=sign_up_dto.user_name, email=sign_up_dto.email, password=password, login_type=login_type)

        user = await self.user_repository.create_user(new_user)

        return user
            