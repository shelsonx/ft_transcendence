from django.urls import path

from .repositories.user_repository import UserRepository
from .repositories.login_type_repository import LoginTypeRepository
from .services.jwt_service import JWTService
from .services.http_client import HttpClient
from .services.sign_in_up_oauth42 import SignInOAuth42Service

from .use_cases.get_user_usecase import GetUserUseCase
from .use_cases.edit_user_usecase import EditUserUseCase
from .use_cases.delete_user_usecase import DeleteUserUseCase
from .use_cases.sign_in_usecase import SignInUseCase
from .use_cases.sign_up_usecase import SignUpUseCase
from .interfaces.usecase.base_signup_usecase import BaseSignUpUseCase
from .use_cases.get_access_token_42_usecase import GetAccessToken42UseCase
from .use_cases.validate_access_token_42_usecase import ValidateAccessToken42UseCase
from .use_cases.get_me_42_usecase import GetMe42UseCase
from .controllers.sign_in_controller import SignInController
from .controllers.sign_up_controller import SignUpController
from .controllers.user_controller import UserController
from .controllers.sign_in_oauth42_controller import SignInOAuth42Controller

from .views import SignInView
from .views import SignUpView
from .views import UserView
from .views import GetUserView
from .views import RedirectOAuth42View
from .views import SignInOAuth42View


# repositories
user_repo = UserRepository()
login_type_repo = LoginTypeRepository()

# services
token_service = JWTService()
http_client = HttpClient()

# use cases
sign_in_use_case = SignInUseCase(user_repo, token_service)
base_sign_up_usecase = BaseSignUpUseCase(user_repo, login_type_repo)
sign_up_use_case = SignUpUseCase(user_repo, token_service, login_type_repo)
get_user_usecase = GetUserUseCase(user_repo)
edit_user_usecase = EditUserUseCase(user_repo)
delete_user_usecase = DeleteUserUseCase(user_repo)
get_access_token_42_use_case = GetAccessToken42UseCase(http_client)
validate_access_token_42_use_case = ValidateAccessToken42UseCase(http_client)
get_me_42_use_case = GetMe42UseCase(http_client)

# services
sign_in_oauth42_service = SignInOAuth42Service(user_repo, token_service, base_sign_up_usecase)

# controllers
sign_up_controller = SignUpController(sign_up_use_case)
sign_in_controller = SignInController(sign_in_use_case)
user_controller = UserController(
    get_user_usecase=get_user_usecase,
    edit_user_usecase=edit_user_usecase, 
    delete_user_usecase=delete_user_usecase
)
sign_in_oauth42_controller = SignInOAuth42Controller(
    http_client=http_client, 
    get_access_token_42_use_case=get_access_token_42_use_case, 
    validate_access_token_42_use_case=validate_access_token_42_use_case, 
    get_me_42_use_case=get_me_42_use_case,
    sign_in_oauth42_service=sign_in_oauth42_service
)

urlpatterns = [
    path("sign-in/", SignInView.as_view(sign_in_controller=sign_in_controller)),
    path("redirect-42", RedirectOAuth42View.as_view()),
    path("sign-up/", SignUpView.as_view(sign_up_controller=sign_up_controller)),
    path("user/", GetUserView.as_view(user_controller=user_controller)),
    path("user/<uuid:user_id>", UserView.as_view(user_controller=user_controller)),
    path("sign-in-42/", SignInOAuth42View.as_view(sign_in_oauth42_controller=sign_in_oauth42_controller))
]