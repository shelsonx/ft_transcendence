from ..interfaces.repositories.auth_repository import IAuthRepository
from ..interfaces.services import ITokenService

from ..exceptions import UserNotFoundEception, InvalidPasswordException

class SignInUseCase:

    def __init__(self, user_repository: IAuthRepository, token_service: ITokenService):
        self.user_repository = user_repository
        self.token_service = token_service

    def execute(self, email, password):
        user = self.user_repository.get_by_email(email)

        if user is None:
            raise UserNotFoundEception()

        if not user.check_password(password):
            raise InvalidPasswordException()

        token = self.token_service.create_token(user)
        return token