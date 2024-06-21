from django import forms

from core.models import GamePlayer

class UpdateGamePlayerForm(forms.ModelForm):

    class Meta:
        model = GamePlayer
        fields = ["score"]
