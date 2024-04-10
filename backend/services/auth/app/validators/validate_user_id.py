from ..exceptions.forbidden_exception import ForbiddenException


def validate_user_id(*args, **kwargs) -> None:
    user_id = kwargs.get("user_id")
    request = args[1]
    if request.current_user.sub != str(user_id):
        raise ForbiddenException()
