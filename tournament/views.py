
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DeleteView
import dawnotc.matchmaking as dm
import dawnotc.classes as dc
from django.views.generic import TemplateView
from tournament.models import *
# Create your views here.


class DayView(TemplateView):
    day = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["FFA"] = FFaMatch.objects.filter(day = self.day)
        context["1v1"] = OvOMatch.objects.filter(day = self.day)

        return context


class MainView(View):
    def get(self, request):
        return render(request, 'matchmaking/matchmaking.html', {"object_list":FFaMatch.objects.all()})


class GenMatchesView(View):
    def post(self, request):
        # matchmaking method was designed with a different format in mind. let's convert to that format before
        # using it
        day = 1
        amount = 2
        dawnplayers = {}
        for p in Player.objects.all():
            dmp = dc.Player(p.name, p.bracket, 0, p.team.id)
            dmp.availability = p.availability
            # TODO doesn't care about preference yet
            # TODO get matches assigned and played
            dawnplayers[p.name] = dmp
        result = dm.generate_matches(dawnplayers, amount, day)
        for match in result:
            djangoplayers = []
            for p in match.players:
                djangoplayers.append(get_object_or_404(Player, name=p.name))
            m = FFaMatch(day=day, location="M")
            m.player1 = djangoplayers[0]
            m.player2 = djangoplayers[1]
            m.player3 = djangoplayers[2]
            m.player4 = djangoplayers[3]
            m.save()

        #return render(request, "matchmaking/matchmaking.html", {"object_list":result})
        return redirect('matchmaking-root')

    def get(self, request):
        return HttpResponse("How did this happen?")


class RemoveMatch(DeleteView):
    model = FFaMatch


class MatchView(View):
    def get(self, request, match_id=None):
        dummy_t1 = Team(name="Alpacas")
        dummy_t2 = Team(name="Beltalawda")
        dummy_t3 = Team(name="Circus")
        dummy_t4 = Team(name="Donkeys")
        dummy_p1 = Player(name="Asimov", team=dummy_t1, bracket=2, stars=2, preference=0, availability=15)
        dummy_p2 = Player(name="Bradbury", team=dummy_t2, bracket=2, stars=2, preference=0, availability=15)
        dummy_p3 = Player(name="Clarke", team=dummy_t3, bracket=2, stars=2, preference=0, availability=15)
        dummy_p4 = Player(name="Herbert", team=dummy_t4, bracket=2, stars=2, preference=0, availability=15)
        dummy_ffa_match = FFaMatch(player1=dummy_p1, player2=dummy_p2, player3=dummy_p3, player4=dummy_p4, location="M", winner=dummy_p2)
        dummy_1v1_match = OvOMatch(player1=dummy_p1, player2=dummy_p2, location="M", winner=dummy_p2)
        return render(request, "matchmaking/detail.html", {"object_list":[dummy_ffa_match, dummy_1v1_match]})

    def post(self, request):
        return HttpResponse("how did this happen?")