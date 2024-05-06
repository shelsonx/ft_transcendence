from django import forms

from core.models import Game

class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        exclude = ["players", "rules"]

class GameEditForm(GameForm):

    class Meta:
        model = Game
        fields = ["duration", "game_datetime", "status"]
