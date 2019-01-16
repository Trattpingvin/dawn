from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

def validate_preference(val):
#preference is 3 bit value. bit order 0x1 = mars, 0x10 = ceres, 0x100 = io
#bit 0 means veto
    if val<0 or val>7:
        raise ValidationError("%(val)s is not a valid preference", params={'value':val})

def validate_availability(val):
#availability is 4 bit value(one per day) bit order 0x1 = day 1, 0x10 = day 2, 0x100 = day 3, 0x1000 = day 4
#bit 1 means available, 0 means unavailable
    if val<0 or val>15:
        raise ValidationError("%(val)s is not a valid availability", params={'value':val})

class Team(models.Model):
    name = models.CharField(max_length = 128)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name

    def is_available(self, day):
        #day should be in range 1-4, determines if this player is available that day
        flags = [None, 0b1, 0b10, 0b100, 0b1000]
        return bool(availability&flags[day])

    def get_matches(self):
        qs = FFaMatch.objects.filter(has_player(self))
        qs.union(OvOMatch.objects.filter(has_player(self)))
        return qs

class Match(models.Model):
    day = models.IntegerField()
    LOCATIONS = [("M","Mars"), ("C", "Ceres"), ("I", "Io")]
    location = models.CharField(choices=LOCATIONS, max_length = 6)
    winner = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "Match on "+location+" on day "+day #list players too? feels like it would become too big

    class Meta:
        abstract=True

class OvOMatch(Match):
    player1 = models.ForeignKey(Player, related_name="p1", on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name="p2", on_delete=models.CASCADE)

    def has_player(self, p):
        return player1==p or player2==p

class FFaMatch(Match):
    player1 = models.ForeignKey(Player, related_name="player1", on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name="player2", on_delete=models.CASCADE)
    player3 = models.ForeignKey(Player, related_name="player3", on_delete=models.CASCADE)
    player4 = models.ForeignKey(Player, related_name="player4", on_delete=models.CASCADE)

    def has_player(self, p):
        return player1==p or player2==p or player3==p or player4==p

class Award(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(FFaMatch, on_delete=models.CASCADE)
    AWARDS = [("A", "Keen eyes on their stuff"), ("B", "Outstanding Performances"),
    ("C", "Race for the initial markets"), ("D", "Eggs in multiple baskets"),
    ("E", "Commercial Meteorology Experiment"), ("F", "Mind Games")]
    award = models.CharField(choices=AWARDS, max_length = 255)

    def __str__(self):
        return self.player +": "+award 

