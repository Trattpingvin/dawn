from django import forms
from tournament.models import MatchResult, RatingChange, Award, Player


class ScoreMatchForm(forms.Form):
	winner = forms.ModelChoiceField(Player.objects.all())
	bracket_before = forms.IntegerField()
	bracket_after = forms.IntegerField()
	stars_before = forms.IntegerField()
	stars_after = forms.IntegerField()






