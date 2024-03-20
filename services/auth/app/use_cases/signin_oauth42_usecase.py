from ..models.user import User
from ..interfaces.repositories.user_repository import IUserRepository
from ..interfaces.services.token_service import ITokenService
from django.core.exceptions import ObjectDoesNotExist
from ..exceptions import InvalidPasswordException, UserNotFoundException
from ..dtos.sign_in_oauth42_dto import SignInOAuth42Dto
from datetime import datetime
from ..exceptions.token_expired_exception import TokenExpiredException
from ..interfaces.usecase.base_usecase import BaseUseCase

class SignInOAuth42UseCase(BaseUseCase):

    def __init__(self, user_repository: IUserRepository, token_service: ITokenService):
        self.user_repository = user_repository
        self.token_service = token_service

    async def execute(self, sign_inOAuth42_dto: SignInOAuth42Dto):
        #validate 42 token before sign in/up
        try:
            user = await self.user_repository.get_user_by_email(sign_inOAuth42_dto.email)
        except ObjectDoesNotExist:
             raise UserNotFoundException()
        
        if not sign_inOAuth42_dto.is_valid():
            raise TokenExpiredException()
        hours_to_expire = sign_inOAuth42_dto.expire_to_hours()
        token = self.token_service.create_token(user, hours_to_expire)
        return token