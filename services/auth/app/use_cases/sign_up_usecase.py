from ..interfaces.repositories.user_repository import IUserRepository
from ..interfaces.repositories.login_type_repository import ILoginTypeRepository
from ..interfaces.services import ITokenService
from ..constants.login_type_constants import LoginTypeConstants
from ..exceptions import FieldAlreadyExists, InvalidPasswordException
from ..models.user import User
from ..dtos.sign_up_dto import SignUpDto
from django.core.exceptions import ObjectDoesNotExist
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
                raise FieldAlreadyExists(duplicated_field)
        except ObjectDoesNotExist:    
        
            login_type = await self.login_type_repository.get_login_type_by_name(LoginTypeConstants.AUTH_EMAIL)
            new_user = User(user_name=sign_up_dto.user_name, email=sign_up_dto.email, password=sign_up_dto.password, login_type=login_type)
            user = await self.user_repository.create_user(new_user)
            token = self.token_service.create_token(user)

            return token
            