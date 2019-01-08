from django.db import models

# Create your models here.

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

class FFaMatch(models.Model):
	player1 = models.ForeignKey(Player, related_name="player1", on_delete=models.CASCADE)
	player2 = models.ForeignKey(Player, related_name="player2", on_delete=models.CASCADE)
	player3 = models.ForeignKey(Player, related_name="player3", on_delete=models.CASCADE)
	player4 = models.ForeignKey(Player, related_name="player4", on_delete=models.CASCADE)
	LOCATIONS = [("M","Mars"), ("C", "Ceres"), ("I", "Io")]
	location = models.CharField(choices=LOCATIONS, max_length = 6)
	result = models.ForeignKey(Player, null=True, default="", on_delete=models.CASCADE)


