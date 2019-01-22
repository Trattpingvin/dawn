
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
import dawnotc.matchmaking as dm
import dawnotc.classes as dc
from django.views.generic import TemplateView
from tournament.models import *
from tournament.forms import *


class DayView(TemplateView):
    day = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["FFA"] = Match.objects.filter(day=self.day, mode="F")
        context["1v1"] = Match.objects.filter(day=self.day, mode="O")

        return context


class PlayerView(View):
    def get(self, request, player_id=None):

        if player_id:
            player = get_object_or_404(Player, id=player_id)
        else:
            return HttpResponse("Player not chosen")

        winloss = player.get_wins()
        awards = player.format_awards()
        award_score = awards[0]
        score = winloss[0] + award_score
        availability = []
        date = ["Jan 26", "Jan 27", "Feb 2", "Feb 3"]
        for i in range(4):
            if player.is_available(i+1): availability.append(1)
            else: availability.append(0)
        preference = [bool(player.preference&1), bool(player.preference&2), bool(player.preference&4)] #"Mars 1" "Ceres 2" "Io 4"

        return render(request, "playerdetail.html",{
            "player": player, "score": score, "award": awards[1],
            "availability": zip(availability, date), "loc": preference,
            })


class PlayersView(ListView):
    template_name = "players.html"
    model = Team
    #ordering = ['team']
    # not sure why i made this class. in case we need something extra I guess?


class ScoreMatchView(View):
    def get(self, request, match_id=None, num_awards=0):
        if not match_id:
            return HttpResponse("Bad match id")
        match = Match.get(id=match_id)
        if match.result:
            return HttpResponse("Match already scored!")

        scoreform = ScoreMatchForm(match_id, num_awards)
        return render(request, 'matchmaking/scorematch.html', {"scoreform": scoreform})

    def post(self, request):
        import pdb
        pdb.set_trace()
        stuff = request.POST
        form = ScoreMatchForm(stuff)
        if form.is_valid():
            return HttpResponse("Good")    
        return HttpResponse("Not good")
        # in ffa, winner gets 2 stars. in 1v1, winner gets 1 star
        # everyone else loses one star
        # if i go to -1 star bracket is -1 and star = 3
        # if i to to 4+ stars, bracket is +1 and star = 1


class MainView(View):
    def get(self, request):
        return render(request, 'matchmaking/matchmaking.html', {"object_list": Match.objects.all()})


class GenMatchesView(View):
    def post(self, request, amount=2):
        # matchmaking method was designed with a different format in mind. let's convert to that format before
        # using it
        # TODO implement 1v1 matchmaking
        day = 1
        dawnplayers = {}
        db_players = Player.objects.all()
        if len(db_players) < 4:
            return HttpResponse("Not enough players in the database to generate a match")
        for p in db_players:
            dmp = dc.Player(p.name, p.bracket, 0, p.team.id)
            dmp.availability = p.availability
            dmp.matches_played = len(p.get_matches())
            pref = []
            for i in range(3):
                pref.append(bool(p.preference & 1 << i))
            dmp.preference = pref
            
            dawnplayers[p.name] = dmp
        
        result = dm.generate_matches(dawnplayers, amount, day) 

        for match in result:
            djangoplayers = []
            for p in match.players:
                djangoplayers.append(get_object_or_404(Player, name=p.name))
            m = Match(day=day, location=match.location, notes=match.notes, mode="F")
            m.save()
            for p in djangoplayers:
                m.players.add(p)

        return HttpResponse("OK")
        #return redirect('matchmaking-root')
        #return render(request, "matchmaking/matchmaking.html", {"object_list":result})

    def get(self, request):
        return HttpResponse("How did this happen?")


class RemoveMatchView(View):
    def post(self, request, match_id=None):
        match = get_object_or_404(Match, id=match_id)
        match.delete()
        return HttpResponse("OK")


class MatchView(View):
    def get(self, request, match_id=None, rnd=0):
        r = rnd
        if match_id:
            ans = get_object_or_404(Match, id=match_id)
            awd = ans.get_awards()
        else:
            return HttpResponse("shouldn't happen")
        if ans.result:
            for p in ans.players.all():
                p.totalscore = len(ans.get_awards().filter(player=p)) * 0.2 + int(ans.result.winner == p)
        return render(request, "matchmaking/detail.html", {"match": ans, "round": r, "award": awd})

    def post(self, request):
        return HttpResponse("how did this happen?")