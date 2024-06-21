from django import forms
from django.utils.translation import gettext_lazy as _


class ValidationForm(forms.Form):
    # username = forms.CharField(widget=forms.HiddenInput())
    token = forms.CharField(
        max_length=10,
        required=True,
        label=_(""),
        help_text=_("The code was sent to the email registered by the user"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["token"].widget.attrs = {"class": "form-control"}
