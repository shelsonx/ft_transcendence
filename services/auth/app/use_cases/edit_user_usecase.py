from ..validators.password_validator import PasswordValidator
from ..exceptions.field_is_missing_exception import FieldIsMissingException
from ..utils.str_is_empty_or_none import is_string_empty_or_none
from ..models.user import User
from ..interfaces.repositories.user_repository import IUserRepository
from django.core.exceptions import ObjectDoesNotExist
from ..exceptions import InvalidPasswordException, UserNotFoundException
from ..dtos.user_edit_dto import UserEditDto

class EditUserUseCase:

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def validate_password(self, user: User, old_password: str, new_password: str) -> bool:
          is_changing_password = is_string_empty_or_none(new_password)
          if not is_changing_password:
            return True
          if is_changing_password and is_string_empty_or_none(old_password):
              raise FieldIsMissingException("old password is missing")
          if user.check_password(user.old_password):
            raise InvalidPasswordException()
          password_validator = PasswordValidator()
          password_validator.validate(new_password)
          return True
  
    async def execute(self, id: str, user_edit_dto: UserEditDto):
        
        try:
            user = await self.user_repository.get_user_by_id(id)
        except ObjectDoesNotExist:
             raise UserNotFoundException()
        self.validate_password(user, user_edit_dto.old_password, user_edit_dto.password)
        for key in user_edit_dto.__dict__.keys():
            if key != 'old_password' and key != 'password':
                setattr(user, key, getattr(user_edit_dto, key))
        self.user_repository.update_user(user)

        return {
            'id': user.id,
            'user_name': user.user_name,
            'email': user.email,
            'login_type': user.login_type.name,
            'enable_2fa': user.enable_2fa,
        }