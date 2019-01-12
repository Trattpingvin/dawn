from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

def validate_preference(val):
#preference is 3 bit value. bit order 0x1 = mars, 0x10 = ceres, 0x100 = io
#bit 1 means veto
	if val<0 or val>7:
		raise ValidationError("%(val)s is not a valid preference", params={'value':val})

def validate_availability(val):
#availability is 4 bit value(one per day) bit order 0x1 = day 1, 0x10 = day 2, 0x100 = day 3, 0x1000 = day 4
#bit 1 means available, 0 means unavailable
	if val<0 or val>15:
		raise ValidationError("%(val)s is not a valid availability", params={'value':val})

class Team(models.Model):
	name = models.CharField(max_length = 128)

class Tournament(models.Model):
	team1 = models.ForeignKey(Team, related_name="team1", on_delete=models.CASCADE)
	team2 = models.ForeignKey(Team, related_name="team2", on_delete=models.CASCADE)
	team3 = models.ForeignKey(Team, related_name="team3", on_delete=models.CASCADE)
	team4 = models.ForeignKey(Team, related_name="team4", on_delete=models.CASCADE)

class Player(models.Model):
	name = models.CharField(primary_key=True, max_length = 40)
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	bracket = models.IntegerField()
	stars = models.IntegerField()
	preference = models.IntegerField(validators = [validate_preference])
	availability = models.IntegerField(validators = [validate_availability])

class Match(models.Model):
	LOCATIONS = [("M","Mars"), ("C", "Ceres"), ("I", "Io")]
	location = models.CharField(choices=LOCATIONS, max_length = 6)
	winner = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
	class Meta:
		abstract=True

class OvOMatch(Match):
	player1 = models.ForeignKey(Player, related_name="p1", on_delete=models.CASCADE)
	player2 = models.ForeignKey(Player, related_name="p2", on_delete=models.CASCADE)

class FFaMatch(Match):
	player1 = models.ForeignKey(Player, related_name="player1", on_delete=models.CASCADE)
	player2 = models.ForeignKey(Player, related_name="player2", on_delete=models.CASCADE)
	player3 = models.ForeignKey(Player, related_name="player3", on_delete=models.CASCADE)
	player4 = models.ForeignKey(Player, related_name="player4", on_delete=models.CASCADE)

class Award(models.Model):
	player = models.ForeignKey(Player, on_delete=models.CASCADE)
	match = models.ForeignKey(FFaMatch, on_delete=models.CASCADE)
	AWARDS = [("A", "Keen eyes on their stuff"), ("B", "Outstanding Performances"),
	("C", "Race for the initial markets"), ("D", "Eggs in multiple baskets"),
	("E", "Commercial Meteorology Experiment"), ("F", "Mind Games")]
	award = models.CharField(choices=AWARDS, max_length = 255)

