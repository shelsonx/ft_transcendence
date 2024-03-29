from django.test import TestCase
from unittest.mock import AsyncMock, patch, Mock
from ...models import User
from ...models.login_type import LoginType
from ...constants.login_type_constants import LoginTypeConstants
from ...use_cases.sign_in_usecase import SignInUseCase
from ...interfaces.services.two_factor_service import ITwoFactorService
from ...interfaces.repositories.user_repository import IUserRepository
from ...interfaces.services.token_service import ITokenService
from ...dtos.sign_in_dto import SignInDto
from ...interfaces.usecase.base_usecase import BaseUseCase
from asgiref.sync import async_to_sync


class SignInUseCaseTestCase(TestCase):

    @patch("app.interfaces.repositories.user_repository.IUserRepository")
    @patch("app.interfaces.services.token_service.ITokenService")
    @patch("app.interfaces.services.two_factor_service.ITwoFactorService")
    @async_to_sync
    async def test_sign_in_usecase_return_success(
        self, user_repository_mock, token_service_mock, two_factor_service_mock
    ):
        login_type = LoginType(id=1, name=LoginTypeConstants.AUTH_EMAIL)
        user = User(
            user_name="bruno",
            email="brunobonaldi@gmail.com",
            login_type=login_type,
            enable_2fa=False,
            password="123456",
            is_active=True,
        )
        user.check_password = Mock(return_value=True)
        user_repository_mock.get_user_by_email = AsyncMock(return_value=user)
        token_service_mock.create_token.return_value = "token"
        two_factor_service_mock.validate_and_delete_two_factor = AsyncMock(
            return_value=True
        )
        sign_in_usecase = SignInUseCase(
            user_repository_mock, token_service_mock, two_factor_service_mock
        )
        sign_in_dto = SignInDto(email=user.email, password=user.password)
        result = await sign_in_usecase.execute(sign_in_dto)
        self.assertEqual(result, "token")
