from ..interfaces.repositories.user_repository import IUserRepository
from ..interfaces.services.token_service import ITokenService
from django.core.exceptions import ObjectDoesNotExist
from ..exceptions import InvalidPasswordException, UserNotFoundException
from ..dtos.sign_in_dto import SignInDto
from ..interfaces.usecase.base_usecase import BaseUseCase

class SignInUseCase(BaseUseCase):

    def __init__(self, user_repository: IUserRepository, token_service: ITokenService):
        self.user_repository = user_repository
        self.token_service = token_service

    async def execute(self, sign_in_dto: SignInDto):
        try:
            user = await self.user_repository.get_user_by_email(sign_in_dto.email)
        except ObjectDoesNotExist:
             raise UserNotFoundException()
        
        if not user.check_password(sign_in_dto.password):
            raise InvalidPasswordException()

        token = self.token_service.create_token(user)
        return token