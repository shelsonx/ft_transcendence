from ..utils.validate_model_async import validate_model_async
from ..validators.password_validator import PasswordValidator
from ..exceptions.field_is_missing_exception import FieldIsMissingException
from ..utils.str_is_empty_or_none import is_string_empty_or_none
from ..utils.has_value import has_value
from ..models.user import User
from ..interfaces.repositories.user_repository import IUserRepository
from django.core.exceptions import ObjectDoesNotExist
from ..exceptions import InvalidPasswordException, UserNotFoundException
from ..dtos.user_edit_dto import UserEditDto
from ..utils.call_async import call_async
from asgiref.sync import sync_to_async
from ..interfaces.usecase.base_usecase import BaseUseCase
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

class EditUserUseCase(BaseUseCase):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def validate_password(
        self, user: User, old_password: str, new_password: str
    ) -> bool:
        is_changing_password = not is_string_empty_or_none(new_password)
        if not is_changing_password:
            return True
        if is_changing_password and is_string_empty_or_none(old_password):
            old_pass_missing = _("old password is missing")
            raise FieldIsMissingException(old_pass_missing)
        if not user.check_password(old_password):
            raise InvalidPasswordException()
        password_validator = PasswordValidator()
        password_validator.validate(new_password)
        return True

    async def execute(self, id: str, user_edit_dto: UserEditDto):
        user = None
        try:
            user = await self.user_repository.get_user_by_id(id)
        except ObjectDoesNotExist:
            raise UserNotFoundException()

        self.validate_password(user, user_edit_dto.old_password, user_edit_dto.password)
        if has_value(user_edit_dto.password):
            user_edit_dto.password = make_password(user_edit_dto.password)
        one_of_the_fields_changed = False
        for key in user_edit_dto.__dict__.keys():
            if key.startswith("_") or key == "old_password" or key == "email":
                continue
            new_value = getattr(user_edit_dto, key)
            if has_value(new_value):
                one_of_the_fields_changed = True
                setattr(user, key, new_value)

        if not one_of_the_fields_changed:
            return await call_async(user.to_safe_dict)

        await validate_model_async(user)
        update_user = await self.user_repository.update_user(user)

        return await call_async(update_user.to_safe_dict)
