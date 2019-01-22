from django import forms
from tournament.models import *
from tournament.choices import AWARDS


class ScoreMatchForm(forms.Form):
	def __init__(self, match_id, num_awards, *args, **kwargs):
		super(forms.Form, self).__init__(*args, **kwargs)
		num_awards = num_awards
		match = Match.objects.get(id=match_id)
		players = match.players.all()
		self.fields['winner'] = forms.ModelChoiceField(players)

		for i in range(num_awards):
			self.fields['award_winner-' + str(i)] = forms.ModelChoiceField(players)
			self.fields['award_type-' + str(i)] = forms.ChoiceField(choices=AWARDS)







