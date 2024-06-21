from typing import Any
from django import forms
from django.utils.translation import gettext_lazy as _

from core.models import Tournament, TournamentType, TournamentPlayer


class TournamentForm(forms.ModelForm):

    class Meta:
        model = Tournament
        fields = [
            "name",
            "tournament_type",
            "number_of_players",
            "number_of_rounds",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs = {"class": "form-control"}
        self.fields["tournament_type"].widget.attrs = {"class": "select form-select"}
        self.fields["number_of_players"].widget.attrs = {"class": "form-control"}
        # self.fields["number_of_players"].widget = forms.HiddenInput(
        #     attrs={"class": "form-control"}
        # )
        self.fields["number_of_rounds"].widget.attrs = {"class": "form-control"}
        self.fields["tournament_type"].initial = TournamentType.ROUND_ROBIN

        tournament_type = self["tournament_type"].value()
        if tournament_type == TournamentType.CHALLENGE:
            self.fields["number_of_players"].disabled = True
            self.fields["number_of_players"].initial = 2
            self.fields["number_of_rounds"].initial = 3
        if tournament_type == TournamentType.ROUND_ROBIN:
            self.fields["number_of_rounds"].disabled = True
            self.fields["number_of_players"].initial = 3
            self.fields["number_of_rounds"].initial = 3

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        tournament_type = cleaned_data["tournament_type"]
        number_of_players = cleaned_data["number_of_players"]
        number_of_rounds = cleaned_data["number_of_rounds"]
        match tournament_type:
            case TournamentType.CHALLENGE:
                if number_of_players != 2:
                    msg = _("Challenge tournament can have only 2 players")
                    self.add_error("number_of_players", forms.ValidationError(msg))
                if number_of_rounds < 3:
                    msg = _("Challenge tournament must have at least 3 rounds")
                    self.add_error("number_of_rounds", forms.ValidationError(msg))
            case TournamentType.ROUND_ROBIN:
                if number_of_players < 3:
                    msg = _("Round Robin tournaments needs at least 3 players")
                    self.add_error("number_of_players", forms.ValidationError(msg))
                if number_of_players > 42:
                    msg = _("Maximum number of players for Round Robin is 42")
                    self.add_error("number_of_players", forms.ValidationError(msg))

        return cleaned_data


class TournamentPlayerForm(forms.ModelForm):
    class Meta:
        model = TournamentPlayer
        fields = ["alias_name"]

    username = forms.CharField(max_length=50)

    field_order = ["username", "alias_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs = {"class": "form-control"}
        self.fields["alias_name"].widget.attrs = {"class": "form-control"}
        self.fields["alias_name"].required = False

class UpdateTournamentForm(TournamentForm):

    class Meta:
        model = Tournament
        fields = [
            "tournament_type",
            "number_of_players",
            "number_of_rounds",
        ]
