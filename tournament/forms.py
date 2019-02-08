from django import forms
from tournament.models import *
from tournament.choices import AWARDS


def get_scorematch_form(players):
	class ScoreMatchForm(forms.Form):
		matchwinner = forms.ModelChoiceField(players)
	return forms.formset_factory(ScoreMatchForm)


def get_award_formset(players):
	class ScoreAwardForm(forms.Form):
		winner = forms.ModelChoiceField(players)
		award = forms.ChoiceField(choices=AWARDS)
	return forms.formset_factory(ScoreAwardForm, extra=0)








