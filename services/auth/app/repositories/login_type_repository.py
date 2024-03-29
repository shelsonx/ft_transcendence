from ..models.login_type import LoginType
from ..interfaces.repositories.login_type_repository import ILoginTypeRepository


class LoginTypeRepository(ILoginTypeRepository):

    async def get_login_type_by_name(self, name: str) -> LoginType:
        return await LoginType.objects.aget(name=name)
