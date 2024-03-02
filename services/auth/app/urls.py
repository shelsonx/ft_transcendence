from django.urls import path

from .repositories.user_repository import UserRepository
from .repositories.login_type_repository import LoginTypeRepository
from .services.jwt_service import JWTService
from .use_cases.edit_user_usecase import EditUserUseCase
from .use_cases.sign_in_usecase import SignInUseCase
from .use_cases.sign_up_usecase import SignUpUseCase
from .controllers.sign_in_controller import SignInController
from .controllers.sign_up_controller import SignUpController
from .controllers.user_controller import UserController
from .views import SignInView
from .views import SignUpView
from .views import UserView

user_repo = UserRepository()
login_type_repo = LoginTypeRepository()
token_service = JWTService()
sign_in_use_case = SignInUseCase(user_repo, token_service)
sign_up_use_case = SignUpUseCase(user_repo, token_service, login_type_repo)
sign_in_controller = SignInController(sign_in_use_case)
sign_up_controller = SignUpController(sign_up_use_case)
edit_user_usecase = EditUserUseCase(user_repo)
user_controller = UserController(edit_user_usecase=edit_user_usecase, delete_user_usecase=None)
urlpatterns = [
    path("sign-in/", SignInView.as_view(sign_in_controller=sign_in_controller)),
    path("sign-up/", SignUpView.as_view(sign_up_controller=sign_up_controller)),
    path("user/<uuid:user_id>", UserView.as_view(user_controller=user_controller))
]