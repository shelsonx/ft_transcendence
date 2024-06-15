from abc import ABC, abstractmethod
from datetime import timedelta
from ..repositories.two_factor_repository import ITwoFactorRepository
from ...exceptions.two_factor_exception import TwoFactorCodeException
from ...models.two_factor import TwoFactor
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

class ITwoFactorService(ABC):

    def __init__(self, two_factor_repository: ITwoFactorRepository):
        self.two_factor_repository = two_factor_repository

    async def add_two_factor(self, user_id: str):
        two_factor = TwoFactor(code=self.generate_code(), user_id=user_id)
        return await self.two_factor_repository.add_two_factor(two_factor)

    @abstractmethod
    def generate_code(self) -> str:
        pass

    @abstractmethod
    async def validate_code(self, user_id: str, code: str) -> bool:
        pass

    @abstractmethod
    def notify_user(self, email: str, code: str) -> None:
        pass

    async def send_code_to_user(self, user_id: str, email: str) -> None:
        try:
            two_factor_code = (
                await self.two_factor_repository.find_two_factor_by_user_id(user_id)
            )
            seconds_to_wait = 60
            if not two_factor_code.can_send_code(seconds_to_wait):
                message = _("You need to wait %(seconds_to_wait)s seconds before sending a new code") % {'seconds_to_wait': seconds_to_wait}
                raise TwoFactorCodeException(message)
        except TwoFactor.DoesNotExist:
            pass
        await self.two_factor_repository.delete_two_factor_by_user_id(user_id)
        two_factor_dto = await self.add_two_factor(user_id)
        self.notify_user(email, two_factor_dto.code)

    async def validate_and_delete_two_factor(self, user_id: str, code: str) -> bool:
        is_valid = await self.validate_code(user_id, code)
        if is_valid:
            await self.delete_two_factor(user_id)
        return is_valid

    async def delete_two_factor(self, user_id: str) -> None:
        await self.two_factor_repository.delete_two_factor_by_user_id(user_id)
