from ..repositories.user_repository import IUserRepository
from ..repositories.login_type_repository import ILoginTypeRepository
from ..services import ITokenService
from ...constants.login_type_constants import LoginTypeConstants
from ...exceptions import FieldAlreadyExistsException, NotValidPasswordException
from ...models.user import User
from ..dtos.base_sign_up_dto import BaseSignUpDto
from django.core.exceptions import ObjectDoesNotExist
from ...validators.password_validator import PasswordValidator
from .base_usecase import BaseUseCase
from django.utils.translation import gettext_lazy as _


class BaseSignUpUseCase(BaseUseCase):

    def __init__(
        self,
        user_repository: IUserRepository,
        login_type_repository: ILoginTypeRepository,
    ):
        self.user_repository = user_repository
        self.login_type_repository = login_type_repository

    async def execute(
        self,
        sign_up_dto: BaseSignUpDto,
        password: str = None,
        login_type: str = LoginTypeConstants.AUTH_EMAIL,
        is_active=False,
    ) -> User:

        if password is None and login_type == LoginTypeConstants.AUTH_EMAIL:
            pass_required = _("Password is required for email sign up")
            raise NotValidPasswordException(
                message=pass_required
            )
        login_type = await self.login_type_repository.get_login_type_by_name(login_type)

        if password is not None:
            password_validator = PasswordValidator()
            password_validator.validate(password=password)

        new_user = User(
            user_name=sign_up_dto.user_name,
            email=sign_up_dto.email,
            password=password,
            login_type=login_type,
            is_active=is_active,
        )

        user = await self.user_repository.create_user(new_user)

        return user
