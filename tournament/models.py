from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
from tournament.choices import AWARDS

def validate_preference(val):
    # preference is 3 bit value. bit order 0x1 = mars, 0x10 = ceres, 0x100 = io
    # bit 0 means veto
    if val < 0 or val > 7:
        raise ValidationError("%(val)s is not a valid preference", params={'value':val})


def validate_availability(val):
    # availability is 4 bit value(one per day) bit order 0x1 = day 1, 0x10 = day 2, 0x100 = day 3, 0x1000 = day 4
    # bit 1 means available, 0 means unavailable
    if val < 0 or val > 15:
        raise ValidationError("%(val)s is not a valid availability", params={'value':val})


class Team(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def get_players(self):
        return Player.objects.filter(team=self).order_by('-bracket', 'stars', Lower('name').asc())


class Tournament(models.Model):
    team1 = models.ForeignKey(Team, related_name="team1", on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name="team2", on_delete=models.CASCADE)
    team3 = models.ForeignKey(Team, related_name="team3", on_delete=models.CASCADE)
    team4 = models.ForeignKey(Team, related_name="team4", on_delete=models.CASCADE)


class Player(models.Model):
    name = models.CharField(max_length=60)  # steam name
    discordname = models.CharField(max_length=60, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    bracket = models.IntegerField()
    stars = models.IntegerField()
    preference = models.IntegerField(validators = [validate_preference])
    availability = models.IntegerField(validators = [validate_availability])
    will_ffa = models.BooleanField()
    will_1v1 = models.BooleanField()
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name

    def is_available(self, day):
        # day should be in range 1-4, determines if this player is available that day
        flags = [None, 0b1, 0b10, 0b100, 0b1000]
        return bool(self.availability & flags[day])

    def get_matches(self):  # i'm not sure i'm happy with this
        return self.match_set.all()

    def get_num_matches(self):
        return len(self.get_matches())

    def get_score(self):
        score = self.format_awards()[0] + self.get_wins()[0]
        int_score = int(score)
        if score == int_score: return int_score
        else: return round(score,1)

    def get_wins(self):
        qs = self.get_matches()
        wins = 0
        losses = 0
        for m in qs:
            if m.result:
                if m.result.winner == self:
                    wins += 1
                else:
                    losses += 1

        return wins, losses 

    def get_awards(self):
        return Award.objects.filter(player=self)

    def format_awards(self):
        awardsdict = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}
        awardnames = ["Keen Eyes on Their Stuff", "Outstanding Performances", "Race for the Initial Markets", "Eggs in Multiple Baskets", "Commercial Meteorology Experiment", "Mind Games"]
        for award in self.get_awards():
            awardsdict[award.award] += 1
        awardscores = [x/5 for x in awardsdict.values()]
        return sum(0.2*n for n in awardsdict.values()), zip(awardnames, awardsdict.values(), awardscores)


class MatchResult(models.Model):
    winner = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return self.winner.name + " won match " + str(self.match)


class RatingChange(models.Model):
    matchresult = models.ForeignKey(MatchResult, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    bracket_before = models.IntegerField()
    bracket_after = models.IntegerField()
    stars_before = models.IntegerField()
    stars_after = models.IntegerField()

    def get_bracket_diff(self):
        return self.bracket_after-self.bracket_before

    def get_stars_diff(self):
        return self.stars_after-self.stars_before


class Match(models.Model):
    day = models.IntegerField()
    LOCATIONS = [("M", "Mars"), ("C", "Ceres"), ("I", "Io")]
    location = models.CharField(choices=LOCATIONS, max_length=6)
    result = models.OneToOneField(MatchResult, null=True, blank=True, on_delete=models.CASCADE)
    notes = models.CharField(max_length=1024, default="", blank=True, null=True)
    players = models.ManyToManyField(Player)
    MODES = [("O", "1v1"), ("F", "FFA")]
    mode = models.CharField(choices=MODES, max_length=1)
    url = models.URLField(null=True, blank=True)
    published = models.BooleanField()
    seed = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)

    def __str__(self):
        ans = self.get_location_display()+", day "+str(self.day)+" round +"+str(self.round)+": "+", ".join((n.name for n in self.players.all()))
        return ans

    def get_awards(self):
        return Award.objects.filter(match=self.result)

    def has_player(self, p):
        return p in self.players

    def get_players(self):
        return self.players.all()


class Award(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match = models.ForeignKey(MatchResult, on_delete=models.CASCADE)

    award = models.CharField(choices=AWARDS, max_length=1)

    def __str__(self):
        return self.player.name+": "+self.get_award_display()
