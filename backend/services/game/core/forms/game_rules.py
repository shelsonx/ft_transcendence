from django import forms

from core.models import GameRules


class GameRulesForm(forms.ModelForm):

    class Meta:
        model = GameRules
        # fields = "__all__"
        fields = ["rule_type", "points_to_win", "game_total_points", "max_duration"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["rule_type"].widget.attrs = {"class": "select form-select"}
        self.fields["points_to_win"].widget.attrs = {"class": "form-control"}
        self.fields["game_total_points"].widget.attrs = {"class": "form-control"}
        self.fields["max_duration"].widget.attrs = {"class": "form-control"}
