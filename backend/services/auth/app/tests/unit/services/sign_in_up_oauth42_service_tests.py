from django.test import TestCase
from unittest.mock import AsyncMock, patch
from asgiref.sync import async_to_sync
from ....models import User
from django.contrib.auth.hashers import make_password
from ....interfaces.repositories.user_repository import IUserRepository
from ....interfaces.services.token_service import ITokenService
from ....interfaces.services.two_factor_service import ITwoFactorService
from ....interfaces.usecase.base_sign_up_usecase import BaseSignUpUseCase
from ....interfaces.usecase.base_sign_in_usecase import BaseSignInUseCase
from ....services.sign_in_up_oauth42_service import SignInOAuth42Service
from ....dtos.sign_in_oauth42_dto import SignInUpOAuth42Dto
from ....models.login_type import LoginType
from ....constants.login_type_constants import LoginTypeConstants
from ....dtos.sign_in_dto import SignInResultDto
from ....exceptions.token_expired_exception import TokenExpiredException
from ....exceptions import FieldAlreadyExistsException


class SignInOAuth42ServiceTests(TestCase):

    @patch("app.interfaces.repositories.user_repository.IUserRepository")
    @patch("app.interfaces.usecase.base_sign_up_usecase.BaseSignUpUseCase")
    @patch("app.interfaces.usecase.base_sign_in_usecase.BaseSignInUseCase")
    def setUp(
        self,
        user_repository_mock: IUserRepository,
        base_sign_up_usecase_mock: BaseSignUpUseCase,
        base_sign_in_usecase_mock: BaseSignInUseCase,
    ):
        self.user_repository_mock = user_repository_mock
        self.base_sign_up_usecase_mock = base_sign_up_usecase_mock
        self.base_sign_in_usecase_mock = base_sign_in_usecase_mock
        self.sign_in_oauth42_service = SignInOAuth42Service(
            self.user_repository_mock,
            self.base_sign_up_usecase_mock,
            self.base_sign_in_usecase_mock,
        )

    @async_to_sync
    async def test_sign_in_oauth42_service_return_success_user_token_not_temporary(
        self,
    ):
        login_type = LoginType(id=2, name=LoginTypeConstants.AUTH_42)
        user = User(
            user_name="bruno",
            email="bruno@gmail.com",
            login_type=login_type,
            enable_2fa=False,
            password=None,
            is_active=True,
        )
        sign_in_up_oath42_dto = SignInUpOAuth42Dto(
            email="bruno@gmail.com",
            access_token="123456",
            expires_in=3600,
            user_name="bruno",
        )
        sign_in_result_dto = SignInResultDto(
            token="token", is_temporary_token=False, email=user.email
        )

        self.user_repository_mock.get_user_by_email = AsyncMock(return_value=user)
        self.base_sign_up_usecase_mock.execute = AsyncMock(return_value=user)
        self.base_sign_in_usecase_mock.execute = AsyncMock(
            return_value=sign_in_result_dto
        )
        self.user_repository_mock.update_user = AsyncMock(return_value=user)
        result = await self.sign_in_oauth42_service.execute(sign_in_up_oath42_dto)
        self.assertEqual(result, sign_in_result_dto)

    @async_to_sync
    async def test_sign_in_oauth42_service_return_success_user_token_temporary(self):
        login_type = LoginType(id=2, name=LoginTypeConstants.AUTH_42)
        user = User(
            user_name="bruno",
            email="bruno@gmail.com",
            login_type=login_type,
            enable_2fa=True,
            password=None,
            is_active=True,
        )
        sign_in_up_oath42_dto = SignInUpOAuth42Dto(
            email="bruno@gmail.com",
            access_token="123456",
            expires_in=3600,
            user_name="bruno",
        )
        sign_in_result_dto = SignInResultDto(
            token="token", is_temporary_token=True, email=user.email
        )

        self.user_repository_mock.get_user_by_email = AsyncMock(return_value=user)
        self.base_sign_in_usecase_mock.execute = AsyncMock(
            return_value=sign_in_result_dto
        )
        result = await self.sign_in_oauth42_service.execute(sign_in_up_oath42_dto)
        self.assertEqual(result, sign_in_result_dto)

    @async_to_sync
    async def test_sign_in_oauth42_service_return_failed_42token_expired(self):
        sign_in_up_oath42_dto = SignInUpOAuth42Dto(
            email="bruno@gmail.com",
            access_token="123456",
            expires_in=-3600,
            user_name="bruno",
        )

        with self.assertRaises(TokenExpiredException):
            await self.sign_in_oauth42_service.execute(sign_in_up_oath42_dto)

    @async_to_sync
    async def test_sign_in_oauth42_service_return_failed_email_already_exists(self):
        login_type = LoginType(id=2, name=LoginTypeConstants.AUTH_EMAIL)
        user = User(
            user_name="bruno",
            email="bruno@gmail.com",
            login_type=login_type,
            enable_2fa=True,
            password=None,
            is_active=True,
        )
        sign_in_up_oath42_dto = SignInUpOAuth42Dto(
            email="bruno@gmail.com",
            access_token="123456",
            expires_in=3600,
            user_name="bruno",
        )
        sign_in_result_dto = SignInResultDto(
            token="token", is_temporary_token=True, email=user.email
        )

        self.user_repository_mock.get_user_by_email = AsyncMock(return_value=user)
        with self.assertRaises(FieldAlreadyExistsException):
            await self.sign_in_oauth42_service.execute(sign_in_up_oath42_dto)
