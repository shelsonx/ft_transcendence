from ..models.user import User
from ..models.login_type import LoginType
from ..interfaces.repositories.auth_repository import IAuthRepository
from django.contrib.auth.hashers import make_password, check_password

class AuthRepository(IAuthRepository):

  async def get_user_by_username(self, username: str) -> User:
    return await User.objects.aget(user_name=username)
  
  async def get_user_by_email(self, email: str) -> User:
    return await User.objects.aget(email=email)
  
  async def get_user_by_id(self, id: str) -> User:
    return await User.objects.aget(id=id)

  async def create_user(self, user: User) -> User:
    hashed_password = make_password(user.password)
    return await User.objects.acreate(
      user_name=user.user_name,
      email=user.email,
      login_type=LoginType.objects.get(id=user.login_type.id),
      password=hashed_password
    )
  
  async def update_user(self, user: User) -> User:
    await User.objects.filter(id=user.id).aupdate(
      user_name=user.user_name,
      email=user.email,
      login_type=LoginType.objects.get(id=user.login_type.id),
      password=user.password,
      enable_2fa=user.enable_2fa
    )
    return user
  
  async def delete_user(self, id: str) -> bool:
    await User.objects.filter(id=id).adelete()
    return True