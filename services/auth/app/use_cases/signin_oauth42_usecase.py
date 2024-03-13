from ..models.user import User
from ..interfaces.repositories.user_repository import IUserRepository
from ..interfaces.services.token_service import ITokenService
from django.core.exceptions import ObjectDoesNotExist
from ..exceptions import InvalidPasswordException, UserNotFoundException
from ..dtos.sign_in_oauth42_dto import SignInOAuth42Dto
from datetime import datetime

class SignInOAuth42UseCase:

    def __init__(self, user_repository: IUserRepository, token_service: ITokenService):
        self.user_repository = user_repository
        self.token_service = token_service

    async def execute(self, sign_inOAuth42_dto: SignInOAuth42Dto):
        # try:
        #     user = await self.user_repository.get_user_by_email(sign_inOAuth42_dto.email)
        # except ObjectDoesNotExist:
        #      raise UserNotFoundException()
        
        # if not user.check_password(sign_inOAuth42_dto.password):
        #     raise InvalidPasswordException()
        user = User(
          user_name = 'hardcoded_username',
          email = 'hardcoded_email@example.com',
          enable_2fa = False,
          password = 'hardcoded_password',
          created_at = datetime.datetime.now(),
          updated_at = datetime.datetime.now(),
        )
       
        token = self.token_service.create_token(user)
        return token