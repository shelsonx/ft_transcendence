import random

from ..interfaces.services.email_service import IEmailService
from ..models.two_factor import TwoFactor
from ..interfaces.services.two_factor_service import ITwoFactorService
from django.conf import settings
from ..interfaces.repositories.two_factor_game_repository import ITwoFactorGameRepository
from django.utils.translation import gettext_lazy as _
from ..dtos.validate_game_2factor_code_dto import ValidateGame2FactorCodeDto, SendGame2FactorCodeDto

class TwoGameFactorService(ITwoFactorService):

    def __init__(
        self, two_factor_game_repository: ITwoFactorGameRepository, email_service: IEmailService
    ):
        super().__init__(two_factor_game_repository)
        self.email_service = email_service

    def generate_code(self) -> str:
        return str(random.randint(100000, 999999))

    def notify_user(self, email: str, code: str) -> None:
        subject = _("Transcendence Journey - Two Factor Authentication")
        message = _("Your two factor authentication code is %(code)s") % {'code': code}
        self.email_service.send_email(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

    async def validate_code(self, two_factor_code: ValidateGame2FactorCodeDto) -> bool:
        for code, user_requester_id in dict(two_factor_code.code_user_receiver_id).items():
            is_valid = await self.validate_and_delete_two_factor(
                user_requester_id, code=code
            )
            if not is_valid:
                return False
        if two_factor_code.code is None or code == "":
            return False
        try:
            two_factor_code = (
                await self.two_factor_repository.find_two_factor_by_user_id(user_id)
            )
        except TwoFactor.DoesNotExist:
            return False
        return two_factor_code.is_valid(code)
