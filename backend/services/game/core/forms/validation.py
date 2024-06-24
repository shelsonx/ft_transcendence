from django import forms
from django.utils.translation import gettext_lazy as _


class PlayerValidationForm(forms.Form):
    user = forms.UUIDField(widget=forms.HiddenInput())
    token = forms.CharField(
        max_length=10,
        required=True,
        label="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["token"].widget.attrs = {"class": "form-control"}


class PlayerValidationGameForm(PlayerValidationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["token"].help_text = _(
            "The code was sent to the email registered by the user"
        )
