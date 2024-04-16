from django.test import TestCase
from unittest.mock import AsyncMock, patch, Mock
from ....models import User
from ....models.login_type import LoginType
from ....constants.login_type_constants import LoginTypeConstants
from ....use_cases.sign_in_usecase import SignInUseCase
from ....interfaces.services.two_factor_service import ITwoFactorService
from ....interfaces.repositories.user_repository import IUserRepository
from ....interfaces.services.token_service import ITokenService
from ....dtos.sign_in_dto import SignInDto, SignInResultDto
from asgiref.sync import async_to_sync
from django.contrib.auth.hashers import make_password
from ....exceptions.user_not_found_exception import UserNotFoundException
from ....exceptions.user_inactive_exception import UserInactiveException
from ....exceptions.invalid_password_exception import InvalidPasswordException
from ....exceptions.two_factor_exception import TwoFactorCodeException
from ....exceptions.forbidden_exception import ForbiddenException


class SignInUseCaseTestCase(TestCase):

    @patch("app.interfaces.repositories.user_repository.IUserRepository")
    @patch("app.interfaces.services.token_service.ITokenService")
    @patch("app.interfaces.services.two_factor_service.ITwoFactorService")
    def setUp(self, user_repository_mock, token_service_mock, two_factor_service_mock):
        self.user_repository_mock = user_repository_mock
        self.token_service_mock = token_service_mock
        self.two_factor_service_mock = two_factor_service_mock
        self.sign_in_usecase = SignInUseCase(
            self.user_repository_mock,
            self.token_service_mock,
            self.two_factor_service_mock,
        )

    @async_to_sync
    async def test_sign_in_usecase_return_success(self):
        password = "123456"
        login_type = LoginType(id=1, name=LoginTypeConstants.AUTH_EMAIL)
        user = User(
            user_name="bruno",
            email="brunobonaldi@gmail.com",
            login_type=login_type,
            enable_2fa=False,
            password=make_password(password),
            is_active=True,
        )
        self.user_repository_mock.get_user_by_email = AsyncMock(return_value=user)
        self.token_service_mock.create_token.return_value = "token"

        sign_in_dto = SignInDto(email=user.email, password=password)
        result = await self.sign_in_usecase.execute(sign_in_dto)
        self.assertEqual(
            result, SignInResultDto(token="token", is_temporary_token=False, email=user.email).to_dict()
        )
        

    @async_to_sync
    async def test_sign_in_usecase_return_success_with_two_factor(self):
        password = "123456"
        login_type = LoginType(id=1, name=LoginTypeConstants.AUTH_EMAIL)
        user = User(
            user_name="bruno",
            email="brunobonaldi@gmail.com",
            login_type=login_type,
            enable_2fa=True,
            password=make_password(password),
            is_active=True,
        )
        self.user_repository_mock.get_user_by_email = AsyncMock(return_value=user)
        self.token_service_mock.create_token.return_value = "token"
        self.two_factor_service_mock.send_code_to_user = AsyncMock(return_value=None)
        sign_in_dto = SignInDto(
            email=user.email, password=password, two_factor_code="1234"
        )
        result = await self.sign_in_usecase.execute(sign_in_dto)
        self.assertEqual(
            result, SignInResultDto(token="token", is_temporary_token=True, email=user.email).to_dict()
        )

    @async_to_sync
    async def test_sign_in_usecase_return_user_not_found(self):
        self.user_repository_mock.get_user_by_email = AsyncMock(
            side_effect=UserNotFoundException
        )
        sign_in_dto = SignInDto(email="brunon@gmail.com", password="123456")
        with self.assertRaises(UserNotFoundException):
            await self.sign_in_usecase.execute(sign_in_dto)

    @async_to_sync
    async def test_sign_in_usecase_return_user_inactive(self):
        login_type = LoginType(id=1, name=LoginTypeConstants.AUTH_EMAIL)
        password = "123"
        user = User(
            user_name="bruno",
            email="bruno@gmail.com",
            login_type=login_type,
            enable_2fa=False,
            password=make_password(password),
            is_active=False,
        )
        self.user_repository_mock.get_user_by_email = AsyncMock(return_value=user)
        self.token_service_mock.create_token.return_value = "token"
        self.two_factor_service_mock.send_code_to_user = AsyncMock(return_value=None)

        sign_in_dto = SignInDto(email=user.email, password=password)

        result = await self.sign_in_usecase.execute(sign_in_dto)

        self.assertEqual(
            result, SignInResultDto(token="token", is_temporary_token=True, email=user.email).to_dict()
        )

    @async_to_sync
    async def test_sign_in_usecase_return_invalid_password(self):
        login_type = LoginType(id=1, name=LoginTypeConstants.AUTH_EMAIL)
        password = "123"
        user = User(
            user_name="bruno",
            email="bruno@gmail.com",
            login_type=login_type,
            enable_2fa=False,
            password=make_password(password),
            is_active=True,
        )
        self.user_repository_mock.get_user_by_email = AsyncMock(return_value=user)
        sign_in_dto = SignInDto(email=user.email, password="1234")
        with self.assertRaises(InvalidPasswordException):
            await self.sign_in_usecase.execute(sign_in_dto)

    @async_to_sync
    async def test_sign_in_usecase_return_forbidden_exception(self):
        login_type = LoginType(id=1, name=LoginTypeConstants.AUTH_42)
        password = "123"
        user = User(
            user_name="bruno",
            email="bruno@gmail.com",
            login_type=login_type,
            enable_2fa=True,
            password=make_password(password),
            is_active=True,
        )
        self.user_repository_mock.get_user_by_email = AsyncMock(return_value=user)
        with self.assertRaises(ForbiddenException):
            await self.sign_in_usecase.execute(
                SignInDto(email=user.email, password=password)
            )
