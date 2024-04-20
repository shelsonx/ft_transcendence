from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UpperCaseValidator:
    def __init__(self, upper_case_min=1):
        self.upper_case_min = upper_case_min

    def validate(self, password, user=None):
        upper_case_count = sum(1 for c in password if c.isupper())
        if upper_case_count < self.upper_case_min:
            raise ValidationError(
                _(
                    "This password must contain at least %(upper_case_min)d character(s) in uppercase."
                ),
                code="password_too_short",
                params={"upper_case_min": self.upper_case_min},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(upper_case_min)d character(s) in uppercase."
            % {"upper_case_min": self.upper_case_min}
        )
