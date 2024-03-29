from django.test import TestCase
from unittest.mock import AsyncMock, patch
from ...models import User
from ...models.login_type import LoginType
from ...constants.login_type_constants import LoginTypeConstants
from ...use_cases.sign_up_usecase import SignUpUseCase
from ...dtos.sign_up_dto import SignUpDto
from asgiref.sync import async_to_sync
from ...exceptions.field_already_exists_exception import FieldAlreadyExistsException
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from ...interfaces.dtos.base_sign_up_dto import BaseSignUpDto
from ...interfaces.usecase.base_signup_usecase import BaseSignUpUseCase
from ...validators.password_validator import PasswordValidator
from ...entities.validation_data import ValidationData
from ...exceptions.not_valid_password_exception import NotValidPasswordException

class BaseSignUpUseCaseTests(TestCase):

    @patch("app.interfaces.repositories.login_type_repository.ILoginTypeRepository")
    @patch("app.interfaces.repositories.user_repository.IUserRepository")
    def setUp(
        self, login_type_repository_mock, user_repository_mock
    ):
        self.login_type_repository_mock = login_type_repository_mock
        self.user_repository_mock = user_repository_mock
        self.base_sign_in_usecase = BaseSignUpUseCase(
            self.user_repository_mock,
            self.login_type_repository_mock,
        )

    @async_to_sync
    @patch.object(PasswordValidator, "validate")
    async def test_base_sign_up_usecase_return_success_user_email(
        self,
        validate_mock,
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
        self.login_type_repository_mock.get_login_type_by_name = AsyncMock(
            return_value=login_type
        )
        validate_mock.return_value = ValidationData(
            is_success=True, message="Password is valid"
        )
        base_sign_up_dto = BaseSignUpDto(email=user.email, user_name=user.user_name)
        self.user_repository_mock.create_user = AsyncMock(return_value=user)


        result = await self.base_sign_in_usecase.execute(
            sign_up_dto=base_sign_up_dto,
            password=password,
            login_type=login_type.name,
        )
        self.assertEqual(result, user)

    @async_to_sync
    async def test_base_sign_up_usecase_return_success_user_auth42(self):
        login_type = LoginType(id=2, name=LoginTypeConstants.AUTH_42)
        user = User(
            user_name="bruno",
            email="brunobonaldi@gmail.com",
            login_type=login_type,
            enable_2fa=False,
            password=None,
            is_active=True,
        )
        self.login_type_repository_mock.get_login_type_by_name = AsyncMock(
            return_value=login_type
        )
        base_sign_up_dto = BaseSignUpDto(email=user.email, user_name=user.user_name)
        self.user_repository_mock.create_user = AsyncMock(return_value=user)


        result = await self.base_sign_in_usecase.execute(
            sign_up_dto=base_sign_up_dto,
            password=user.password,
            login_type=login_type.name,
            is_active=user.is_active,
        )
        self.assertEqual(result, user)


    @async_to_sync
    @patch.object(PasswordValidator, "validate")
    async def test_base_sign_up_usecase_return_failed_not_valid_password(
        self,
        validate_mock,
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
        self.login_type_repository_mock.get_login_type_by_name = AsyncMock(
            return_value=login_type
        )
        validate_mock.side_effect = NotValidPasswordException(
            message="Password is invalid"
        )
        base_sign_up_dto = BaseSignUpDto(email=user.email, user_name=user.user_name)

        with self.assertRaises(NotValidPasswordException):
            await self.base_sign_in_usecase.execute(
                sign_up_dto=base_sign_up_dto,
                password=password,
                login_type=login_type.name,
            )

    @async_to_sync
    async def test_base_signup_usecase_return_failed_missing_password(self):
        login_type = LoginType(id=1, name=LoginTypeConstants.AUTH_EMAIL)
        user = User(
            user_name="bruno",
            email="brunobonaldi@gmail.com",
            login_type=login_type,
            enable_2fa=False,
            password=None,
            is_active=True,
        )
        with self.assertRaises(NotValidPasswordException):
            await self.base_sign_in_usecase.execute(
                sign_up_dto=BaseSignUpDto(email=user.email, user_name=user.user_name),
                password=user.password,
                login_type=login_type.name,
            )
    