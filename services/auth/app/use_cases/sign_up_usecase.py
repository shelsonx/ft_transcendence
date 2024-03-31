from ..exceptions.two_factor_exception import TwoFactorCodeException
from ..interfaces.services.two_factor_service import ITwoFactorService
from ..exceptions.user_inactive_exception import UserInactiveException
from ..interfaces.repositories.user_repository import IUserRepository
from ..interfaces.repositories.login_type_repository import ILoginTypeRepository
from ..interfaces.services import ITokenService
from ..constants.login_type_constants import LoginTypeConstants
from ..exceptions import FieldAlreadyExistsException
from ..dtos.sign_up_dto import SignUpDto
from ..dtos.two_factor_dto import TwoFactorDto
from ..interfaces.dtos.base_sign_up_dto import BaseSignUpDto
from django.core.exceptions import ObjectDoesNotExist
from ..utils.call_async import call_async

from ..interfaces.usecase.base_sign_up_usecase import BaseSignUpUseCase
from ..interfaces.usecase.base_sign_in_usecase import BaseSignInUseCase


class SignUpUseCase(BaseSignUpUseCase):

    def __init__(
        self,
        user_repository: IUserRepository,
        login_type_repository: ILoginTypeRepository,
        two_factor_service: ITwoFactorService,
        base_sign_in_use_case: BaseSignInUseCase,
    ):
        self.two_factor_service = two_factor_service
        self.base_sign_in_use_case = base_sign_in_use_case
        super().__init__(user_repository, login_type_repository)

    async def execute(self, sign_up_dto: SignUpDto):
        try:
            await self.user_repository.get_user_by_email(email=sign_up_dto.email)
            raise FieldAlreadyExistsException("email")
        except ObjectDoesNotExist:
            base_sign_up_dto = BaseSignUpDto(
                email=sign_up_dto.email, user_name=sign_up_dto.user_name
            )
            new_user = await super().execute(
                sign_up_dto=base_sign_up_dto,
                password=sign_up_dto.password,
                login_type=LoginTypeConstants.AUTH_EMAIL,
            )
            result = await self.base_sign_in_use_case.execute(
                user=new_user, is_temporary_token=True
            )
            return result.to_dict()
