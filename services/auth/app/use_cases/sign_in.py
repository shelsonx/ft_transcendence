from ..interfaces.repositories.user_repository import IUserRepository
from ..interfaces.services import ITokenService

from ..exceptions import UserNotFoundEception, InvalidPasswordException

class SignInUseCase:

    def __init__(self, user_repository: IUserRepository, token_service: ITokenService):
        self.user_repository = user_repository
        self.token_service = token_service

    async def execute(self, email, password):
        user = await self.user_repository.get_user_by_email(email)

        if user is None:
            raise UserNotFoundEception()

        if not user.check_password(password):
            raise InvalidPasswordException()

        token = self.token_service.create_token(user)
        return token