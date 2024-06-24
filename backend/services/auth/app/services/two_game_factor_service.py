import random

from ..exceptions.two_factor_exception import TwoFactorCodeException

from ..interfaces.services.email_service import IEmailService
from ..models.two_factor import TwoFactor
from ..interfaces.services.two_factor_game_service import ITwoGameFactorService
from django.conf import settings
from ..interfaces.repositories.two_factor_game_repository import ITwoFactorGameRepository
from django.utils.translation import gettext_lazy as _
from ..dtos.validate_game_2factor_code_dto import ValidateGame2FactorCodeDto, SendGame2FactorCodeDto

class TwoGameFactorService(ITwoGameFactorService):

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
        try:
            dict_code_user_receiver_id = dict(two_factor_code.code_user_receiver_id)
            two_factor_codes = (
                await self.two_factor_game_repository.find_validate_two_factor_by_game_details(two_factor_code)
            )
            if not two_factor_codes or len(two_factor_codes) == 0:
                raise TwoFactorCodeException(_("Invalid Access Token"))
            codes = dict_code_user_receiver_id.keys()
            if len(two_factor_codes) != len(codes):
                codes_not_found = list(filter(lambda code: code not in two_factor_codes, codes))
                raise TwoFactorCodeException(_("Two factor code not founds %(codes)s") % {"codes": ','.join(codes_not_found)})
        except TwoFactor.DoesNotExist:
            return False

        if two_factor_code is not None:
            await self.two_factor_game_repository.delete_two_factor_by_ids(
                [two_factor.id for two_factor in two_factor_codes]
            )

        return True
