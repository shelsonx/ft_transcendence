from ..interfaces.repositories.user_repository import IUserRepository
from ..interfaces.repositories.login_type_repository import ILoginTypeRepository
from ..interfaces.services import ITokenService
from ..constants.login_type_constants import LoginTypeConstants
from ..exceptions import FieldAlreadyExistsException, InvalidPasswordException
from ..models.user import User
from ..dtos.sign_up_dto import SignUpDto
from ..interfaces.dtos.base_sign_up_dto import BaseSignUpDto
from django.core.exceptions import ObjectDoesNotExist

from ..validators.password_validator import PasswordValidator
from ..interfaces.usecase.base_usecase import BaseUseCase
from ..interfaces.usecase.base_signup_usecase  import BaseSignUpUseCase


class SignUpUseCase(BaseSignUpUseCase):

    def __init__(self, user_repository: IUserRepository, token_service: ITokenService, login_type_repository: ILoginTypeRepository):
        self.token_service = token_service
        super().__init__(user_repository, login_type_repository)

    async def execute(self, sign_up_dto: SignUpDto):
        try:
            user = await self.user_repository.get_user_by_email_or_username(email=sign_up_dto.email, username=sign_up_dto.user_name)
            if user is not None:
                duplicated_field = "email" if user.email == sign_up_dto.email else "user_name"
                raise FieldAlreadyExistsException(duplicated_field)
        except ObjectDoesNotExist:
            base_sign_up_dto = BaseSignUpDto(email=sign_up_dto.email, user_name=sign_up_dto.user_name)
            new_user = await super().execute(
                sign_up_dto=base_sign_up_dto,
                password=sign_up_dto.password, 
                login_type=LoginTypeConstants.AUTH_EMAIL
            )
            token = self.token_service.create_token(new_user)
            return token
                