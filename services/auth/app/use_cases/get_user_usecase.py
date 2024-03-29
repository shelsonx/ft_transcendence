from ..utils.validate_model_async import validate_model_async
from ..validators.password_validator import PasswordValidator
from ..exceptions.field_is_missing_exception import FieldIsMissingException
from ..utils.str_is_empty_or_none import is_string_empty_or_none
from ..utils.has_value import has_value
from ..models.user import User
from ..interfaces.repositories.user_repository import IUserRepository
from django.core.exceptions import ObjectDoesNotExist
from ..exceptions import UserNotFoundException
from ..utils.call_async import call_async
from ..interfaces.usecase.base_usecase import BaseUseCase


class GetUserUseCase(BaseUseCase):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, id: str):
        try:
            user = await self.user_repository.get_user_by_id(id)
            return await call_async(user.to_safe_dict)
        except ObjectDoesNotExist:
            raise UserNotFoundException()
