class UserManagementException(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self):
        return {'status': 'error', 'message': self.message, 'status_code': self.status_code}


class UserDoesNotExistException(UserManagementException):
    def __init__(self, message='User does not exist', status_code=404):
        super().__init__(message, status_code)

class InvalidUUIDException(UserManagementException):
    def __init__(self, message='Invalid UUID', status_code=400):
        super().__init__(message, status_code)

class UserAlreadyExistsException(UserManagementException):
    def __init__(self, message='User already exists', status_code=400):
        super().__init__(message, status_code)

class InvalidFieldException(UserManagementException):
    def __init__(self, message='Invalid field', status_code=400):
        super().__init__(message, status_code)

class MissingParameterException(UserManagementException):
    def __init__(self, parameter, message='Missing parameter', status_code=400):
        self.parameter = parameter
        super().__init__(f'{message}: {parameter}', status_code)

class InvalidJSONDataException(UserManagementException):
    def __init__(self, message='Invalid JSON data', status_code=400):
        super().__init__(message, status_code)

class InvalidFormDataException(UserManagementException):
    def __init__(self, message='Invalid form data', status_code=400):
        super().__init__(message, status_code)