from django import forms

from core.models import GameRules

class GameRulesForm(forms.ModelForm):

    class Meta:
        model = GameRules
        # fields = "__all__"
        fields = ["points_to_win"]
