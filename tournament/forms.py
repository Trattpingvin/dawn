from django import forms
from tournament.models import *


class ScoreMatchForm(forms.Form):
	def __init__(self, match_id, num_awards):
		self.match_id = match_id
		self.num_awards = num_awards
	match = Match.get(id=self.match_id)
	players = match.players.all()
	winner = forms.ModelChoiceField(players)

	self.players = []
	for i, p in enumerate(players):
		self.players.append(p)
		self.fields['bracket_before-' + str(i)] = forms.IntegerField(label="Bracket before for "+p.name)
		self.fields['bracket_after-' + str(i)] = forms.IntegerField(label="Bracket after for "+p.name)
		self.fields['stars_before-' + str(i)] = forms.IntegerField(label="Stars before for "+p.name)
		self.fields['stars_after-' + str(i)] = forms.IntegerField(label="Stars after for "+p.name)
            
		
	for _ in range(num_awards):
		award_winner = forms.ModelChoiceField(players)
		award = forms.ModelChoiceField(Award.objects.all())






