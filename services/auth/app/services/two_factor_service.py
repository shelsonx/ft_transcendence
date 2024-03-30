import random

from ..interfaces.services.email_service import IEmailService
from ..models.two_factor import TwoFactor
from ..interfaces.services.two_factor_service import ITwoFactorService
from django.conf import settings
from ..interfaces.repositories.two_factor_repository import ITwoFactorRepository


class TwoFactorService(ITwoFactorService):

    def __init__(
        self, two_factor_repository: ITwoFactorRepository, email_service: IEmailService
    ):
        super().__init__(two_factor_repository)
        self.email_service = email_service

    def generate_code(self) -> str:
        return str(random.randint(100000, 999999))

    def notify_user(self, email: str, code: str) -> None:
        self.email_service.send_email(
            subject="Transcendence Journey - Two Factor Authentication",
            message=f"Your two factor authentication code is {code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

    async def validate_code(self, user_id: str, code: str) -> bool:
        if code is None or code == "":
            return False
        try:
            two_factor_code = await self.two_factor_repository.find_two_factor_by_user_id(
                user_id
            )
        except TwoFactor.DoesNotExist:
            return False
        return two_factor_code.is_valid(code)
