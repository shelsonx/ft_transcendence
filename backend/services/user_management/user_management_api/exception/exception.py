from django.utils.translation import gettext as _
class UserManagementException(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self):
        return {'status': 'error', 'message': self.message, 'status_code': self.status_code}


class UserDoesNotExistException(UserManagementException):
    user_does_not_exist_message = _('User does not exist')
    def __init__(self, message=user_does_not_exist_message, status_code=404):
        super().__init__(message, status_code)

class InvalidUUIDException(UserManagementException):
    invalid_uuid_message = _('Invalid UUID')
    def __init__(self, message=invalid_uuid_message, status_code=400):
        super().__init__(message, status_code)

class UserAlreadyExistsException(UserManagementException):
    user_already_exists_message = _('User already exists')
    def __init__(self, message=user_already_exists_message, status_code=400):
        super().__init__(message, status_code)

class InvalidFieldException(UserManagementException):
    invalid_field_message = _('Invalid field')
    def __init__(self, message=invalid_field_message, status_code=400):
        super().__init__(message, status_code)

class MissingParameterException(UserManagementException):
    missing_parameter_message = _('Missing parameter')
    def __init__(self, parameter, message=missing_parameter_message, status_code=400):
        self.parameter = parameter
        super().__init__(f'{message}: {parameter}', status_code)

class InvalidJSONDataException(UserManagementException):
    invalid_json_data_message = _('Invalid JSON data')
    def __init__(self, message=invalid_json_data_message, status_code=400):
        super().__init__(message, status_code)

class InvalidFormDataException(UserManagementException):
    invalid_form_data_message = _('Invalid form data')
    def __init__(self, message=invalid_form_data_message, status_code=400):
        super().__init__(message, status_code)

class FriendshipAlreadyExistsException(UserManagementException):
    friendship_already_exists_message = _('Friendship already exists')
    def __init__(self, message=friendship_already_exists_message, status_code=400):
        super().__init__(message, status_code)