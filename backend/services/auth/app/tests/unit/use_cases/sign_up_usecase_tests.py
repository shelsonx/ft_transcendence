from django.test import TestCase
from unittest.mock import AsyncMock, patch

from ....dtos.sign_in_dto import SignInResultDto
from ....models import User
from ....models.login_type import LoginType
from ....constants.login_type_constants import LoginTypeConstants
from ....use_cases.sign_up_usecase import SignUpUseCase
from ....dtos.sign_up_dto import SignUpDto
from asgiref.sync import async_to_sync
from ....exceptions.field_already_exists_exception import FieldAlreadyExistsException
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from ....interfaces.dtos.base_sign_up_dto import BaseSignUpDto
from ....interfaces.usecase.base_sign_up_usecase import BaseSignUpUseCase


class SignUpUseCaseTests(TestCase):

    @patch("app.interfaces.repositories.login_type_repository.ILoginTypeRepository")
    @patch("app.interfaces.repositories.user_repository.IUserRepository")
    @patch("app.interfaces.services.two_factor_service.ITwoFactorService")
    @patch("app.interfaces.usecase.base_sign_in_usecase.BaseSignInUseCase")
    def setUp(
        self,
        login_type_repository_mock,
        user_repository_mock,
        two_factor_service_mock,
        base_sign_in_usecase,
    ):
        self.login_type_repository_mock = login_type_repository_mock
        self.user_repository_mock = user_repository_mock
        self.two_factor_service_mock = two_factor_service_mock
        self.base_sign_in_use_case_mock = base_sign_in_usecase
        self.sign_in_usecase = SignUpUseCase(
            self.user_repository_mock,
            self.login_type_repository_mock,
            self.two_factor_service_mock,
            self.base_sign_in_use_case_mock,
        )

    @async_to_sync
    @patch.object(BaseSignUpUseCase, "execute")
    async def test_sign_up_usecase_return_two_factor_code_sent_to_email(
        self, execute_mock
    ):
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
        mock_execute = AsyncMock(return_value=user)
        self.user_repository_mock.get_user_by_email = AsyncMock(
            side_effect=ObjectDoesNotExist
        )
        base_sign_up_dto = BaseSignUpDto(email=user.email, user_name=user.user_name)
        execute_mock.return_value = mock_execute
        self.two_factor_service_mock.send_code_to_user = AsyncMock(return_value=None)
        sign_in_result = SignInResultDto(
            token="token", is_temporary_token=True, email=user.email
        )
        self.base_sign_in_use_case_mock.execute = AsyncMock(return_value=sign_in_result)
        result = await self.sign_in_usecase.execute(
            SignUpDto(email=user.email, password=password, user_name=user.user_name)
        )
        self.assertEqual(result, sign_in_result.to_dict())

    @async_to_sync
    async def test_sign_up_usecase_return_failed_email_already_exists(self):
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
        with self.assertRaises(FieldAlreadyExistsException):
            await self.sign_in_usecase.execute(
                SignUpDto(email=user.email, password=password, user_name=user.user_name)
            )
