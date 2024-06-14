from django import forms

from core.models import Tournament


class TournamentForm(forms.ModelForm):

    class Meta:
        model = Tournament
        fields = [
            # "name",
            "tournament_type",
            "number_of_players",
            "number_of_rounds",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["name"].widget.attrs = {"class": "form-control"}
        self.fields["tournament_type"].widget.attrs = {"class": "select form-select"}
        self.fields["number_of_players"].widget.attrs = {"class": "form-control"}
        self.fields["number_of_rounds"].widget.attrs = {"class": "form-control"}


class TournamentEditForm(TournamentForm):

    class Meta:
        model = Tournament
        fields = [
            # "name",
            "tournament_type",
            "number_of_players",
            "number_of_rounds",
        ]
