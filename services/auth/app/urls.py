from django.urls import path

from .repositories.user_repository import UserRepository
from .repositories.login_type_repository import LoginTypeRepository
from .services.jwt_service import JWTService
from .use_cases.get_user_usecase import GetUserUseCase
from .use_cases.edit_user_usecase import EditUserUseCase
from .use_cases.delete_user_usecase import DeleteUserUseCase
from .use_cases.sign_in_usecase import SignInUseCase
from .use_cases.sign_up_usecase import SignUpUseCase
from .use_cases.signin_oauth42_usecase import SignInOAuth42UseCase
from .controllers.sign_in_controller import SignInController
from .controllers.sign_up_controller import SignUpController
from .controllers.user_controller import UserController
from .controllers.sign_in_oauth42_controller import SignInOAuth42Controller
from .views import SignInView
from .views import SignUpView
from .views import UserView
from .views import GetUserView
from .views import SignInOAuth42View

# repositories
user_repo = UserRepository()
login_type_repo = LoginTypeRepository()

# services
token_service = JWTService()

# use cases
sign_in_use_case = SignInUseCase(user_repo, token_service)
sign_up_use_case = SignUpUseCase(user_repo, token_service, login_type_repo)
get_user_usecase = GetUserUseCase(user_repo)
edit_user_usecase = EditUserUseCase(user_repo)
delete_user_usecase = DeleteUserUseCase(user_repo)

# controllers
sign_up_controller = SignUpController(sign_up_use_case)
sign_in_controller = SignInController(sign_in_use_case)
user_controller = UserController(
    get_user_usecase=get_user_usecase,
    edit_user_usecase=edit_user_usecase, 
    delete_user_usecase=delete_user_usecase
)
sign_in_oauth42_usecase = SignInOAuth42UseCase(user_repo, token_service)
sign_in_oauth42_controller = SignInOAuth42Controller(sign_in_oauth42_usecase)

urlpatterns = [
    path("sign-in/", SignInView.as_view(sign_in_controller=sign_in_controller)),
    path("sign-in-42", SignInOAuth42View.as_view(sign_in_oauth42_controller=sign_in_oauth42_controller)),
    path("sign-up/", SignUpView.as_view(sign_up_controller=sign_up_controller)),
    path("user/", GetUserView.as_view(user_controller=user_controller)),
    path("user/<uuid:user_id>", UserView.as_view(user_controller=user_controller)),
]