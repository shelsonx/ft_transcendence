from ..models.two_factor import TwoFactor
from ..interfaces.repositories.two_factor_repository import ITwoFactorRepository

class TwoFactorRepository(ITwoFactorRepository):

  async def add_two_factor(self, two_factor: TwoFactor) -> TwoFactor:
    return await two_factor.asave()

  async def delete_two_factor(self, id: str) -> bool:
    return await TwoFactor.objects.filter(id=id).adelete()
