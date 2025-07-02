# predictions/forms.py 

from django import forms
from django.db.models import Q
from django.utils import timezone

from fixtures.models import Team, Player, Matchday
from .models import Prediction

class PredictionForm(forms.ModelForm):
    # insert the new field before potm
    potm_team = forms.ModelChoiceField(
        queryset=Team.objects.none(),
        required=False,
        label="Team for Player of the Matchday",
        empty_label="Select a Team"
    )

    class Meta:
        model = Prediction
        fields = ['favorite_team', 'potm_team', 'potm']
        labels = {
            'favorite_team': 'Favorite National Team',
            'potm': 'Player of the Matchday',
        }

    def __init__(self, *args, matchday=None, **kwargs):
        super().__init__(*args, **kwargs)

        # make everything optional
        self.fields['favorite_team'].required = False
        self.fields['potm_team'].required     = False
        self.fields['potm'].required          = False

        if matchday:
            # restrict both team fields to only those playing this matchday
            teams = Team.objects.filter(
                Q(home_matches__matchday=matchday) |
                Q(away_matches__matchday=matchday)
            ).distinct()

            # favorite team as before
            self.fields['favorite_team'].queryset = teams

            # potm_team uses the same list
            self.fields['potm_team'].queryset = teams

            # potm initially gets *all* players from those teams,
            # JS will filter it down when a team is chosen
            self.fields['potm'].queryset = Player.objects.filter(team__in=teams)

            # adjust label if final
            if matchday.name == Matchday.FINAL:
                self.fields['potm'].label = 'Player of the Tournament'
            else:
                self.fields['potm'].label = 'Player of the Matchday'


class MatchPickForm(forms.Form):
    """
    A standalone Form (not ModelForm) for each match’s two scores.
    We’ll bind .match onto each form in the formset,
    so we can disable it if kickoff_time has passed.
    """
    predicted_home_score = forms.IntegerField(
        label='Home Score',
        min_value=0,
        required=False,
        widget=forms.TextInput(attrs={
            'inputmode': 'numeric',
            'pattern': '[0-9]*',
            'maxlength': '2',
            'placeholder': '0'
        })
    )
    predicted_away_score = forms.IntegerField(
        label='Away Score',
        min_value=0,
        required=False,
        widget=forms.TextInput(attrs={
            'inputmode': 'numeric',
            'pattern': '[0-9]*',
            'maxlength': '2',
            'placeholder': '0'
        })
    )


    def __init__(self, *args, match=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.match = match  # Attach the Match instance

        # If the match has already started, disable the inputs
        if timezone.now() >= self.match.kickoff_time:
            for fld in ('predicted_home_score', 'predicted_away_score'):
                self.fields[fld].widget.attrs['disabled'] = True
                self.fields[fld].required = False


from django.forms import BaseFormSet

class BaseMatchPickFormSet(BaseFormSet):
    """
    We override _construct_form so that each form gets the corresponding match.
    """
    def __init__(self, *args, matches=None, **kwargs):
        self.matches = matches or []
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        """
        Called for each form index i. We inject the correct match.
        """
        kwargs['match'] = self.matches[i]
        return super()._construct_form(i, **kwargs)
