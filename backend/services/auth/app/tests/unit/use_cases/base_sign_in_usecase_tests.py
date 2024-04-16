from django.test import TestCase
from unittest.mock import AsyncMock, patch
from ....models import User
from ....models.login_type import LoginType
from ....constants.login_type_constants import LoginTypeConstants
from asgiref.sync import async_to_sync
from django.contrib.auth.hashers import make_password
from ....interfaces.usecase.base_sign_in_usecase import BaseSignInUseCase
from ....dtos.sign_in_dto import SignInResultDto


class BaseSignInUseCaseTests(TestCase):

    @patch("app.interfaces.services.token_service.ITokenService")
    @patch("app.interfaces.services.two_factor_service.ITwoFactorService")
    def setUp(self, token_service_mock, two_factor_service_mock):
        self.token_service_mock = token_service_mock
        self.two_factor_service_mock = two_factor_service_mock
        self.base_sign_in_usecase = BaseSignInUseCase(
            self.token_service_mock, self.two_factor_service_mock
        )

    @async_to_sync
    async def test_base_sign_in_usecase_return_success_user_token_not_temporary(
        self,
    ):
        password = "123456"
        login_type = LoginType(id=1, name=LoginTypeConstants.AUTH_EMAIL)
        user = User(
            user_name="bruno",
            email="bruno@gmail.com",
            login_type=login_type,
            enable_2fa=False,
            password=make_password(password),
            is_active=True,
        )
        self.token_service_mock.create_token.return_value = "token"
        self.two_factor_service_mock.send_code_to_user = AsyncMock(return_value=None)

        result = await self.base_sign_in_usecase.execute(
            user=user,
            is_temporary_token=False,
        )
        self.assertEqual(
            vars(result), vars(SignInResultDto(token="token", is_temporary_token=False, email=user.email))
        )

    @async_to_sync
    async def test_base_sign_in_usecase_return_success_user_token_temporary(
        self,
    ):
        password = "123456"
        login_type = LoginType(id=1, name=LoginTypeConstants.AUTH_EMAIL)
        user = User(
            user_name="bruno",
            email="bruno@gmail.com",
            login_type=login_type,
            enable_2fa=False,
            password=make_password(password),
            is_active=True,
        )
        self.token_service_mock.create_token.return_value = "token"
        self.two_factor_service_mock.send_code_to_user = AsyncMock(return_value=None)

        result = await self.base_sign_in_usecase.execute(
            user=user,
            is_temporary_token=True,
        )
        self.assertEqual(
            vars(result), vars(SignInResultDto(token="token", is_temporary_token=True, email=user.email))
        )
