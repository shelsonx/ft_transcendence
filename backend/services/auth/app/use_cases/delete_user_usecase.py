from ..interfaces.repositories.user_repository import IUserRepository
from django.core.exceptions import ObjectDoesNotExist
from ..exceptions import UserNotFoundException
from ..interfaces.usecase.base_usecase import BaseUseCase


class DeleteUserUseCase(BaseUseCase):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, id: str) -> bool:
        try:
            user = await self.user_repository.get_user_by_id(id)
            await self.user_repository.delete_user(user.id)
            return True
        except ObjectDoesNotExist:
            raise UserNotFoundException()
