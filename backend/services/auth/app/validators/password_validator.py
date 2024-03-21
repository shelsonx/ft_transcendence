
from typing import Any
from ..interfaces.validator.base_validator import BaseValidator
from .min_length_validator import MinimumLengthValidator
from .upper_case_validator import UpperCaseValidator
from .lower_case_validator import LowerCaseValidator

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from ..exceptions.not_valid_password_exception import NotValidPasswordException
from ..entities.validation_data import ValidationData

class PasswordValidator(BaseValidator):
    
    def __init__(self):
        super().__init__()

    def validate(self, password: str) -> ValidationData:
        try:
            min_len = MinimumLengthValidator()
            upper_case = UpperCaseValidator()
            lower_case = LowerCaseValidator()
            validate_password(password, None, password_validators=[min_len, upper_case, lower_case])
            return ValidationData(is_success=True, message="Password is valid")
        except ValidationError as e:
            raise NotValidPasswordException(e.messages)