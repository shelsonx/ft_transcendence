from ..models.two_factor import TwoFactor
from ..interfaces.repositories.two_factor_repository import ITwoFactorRepository


class TwoFactorRepository(ITwoFactorRepository):

    async def add_two_factor(self, two_factor: TwoFactor) -> TwoFactor:
        return await TwoFactor.objects.acreate(
            code=two_factor.code, user_id=two_factor.user_id
        )

    async def delete_two_factor(self, id: str) -> bool:
        return await TwoFactor.objects.filter(id=id).adelete()

    async def find_two_factor_by_user_id(self, user_id: str) -> TwoFactor:
        return await TwoFactor.objects.aget(user_id=user_id)

    async def delete_two_factor_by_user_id(self, user_id: str) -> bool:
        return await TwoFactor.objects.filter(user_id=user_id).adelete()
