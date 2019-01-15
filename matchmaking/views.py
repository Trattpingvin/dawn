from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
import sys
from django.contrib.admin.views.decorators import staff_member_required
from matchmaking.models import *
from django.views.generic import ListView, DeleteView
import dawnotc.matchmaking as dm
import dawnotc.classes as dc


class MainView(View):
    def get(self, request):
        return render(request, 'matchmaking/matchmaking.html', {"object_list":FFaMatch.objects.all()})

class GenMatchesView(View):
    def post(self, request):
        #matchmaking method was designed with a different format in mind. let's convert to that format before
        # using it
        day = 1
        amount = 2
        dawnplayers = {}
        for p in Player.objects.all():
            dmp = dc.Player(p.name, p.bracket, 0, p.team.id)
            dmp.availability = p.availability
            #TODO doesn't care about preference yet
            #TODO get matches assigned and played
            dawnplayers[p.name] = dmp
        result = dm.generate_matches(dawnplayers, amount, day)
        for match in result:
            djangoplayers = []
            for p in match.players:
                djangoplayers.append(Player.objects.filter(name=p.name))
            m = FFaMatch(day=day, location="M")
            m.player1 = list(djangoplayers[0])[0]
            m.player2 = list(djangoplayers[1])[0]
            m.player3 = list(djangoplayers[2])[0]
            m.player4 = list(djangoplayers[3])[0]
            m.save()

        #return render(request, "matchmaking/matchmaking.html", {"object_list":result})
        return redirect('matchmaking-root')

    def get(self, request):
        return HttpResponse("How did this happen?")

class RemoveMatch(DeleteView):
    model = FFaMatch

class MatchView(View):
    def get(self, request, match_id):
        dummy_t1 = Team(name="t1")
        dummy_t2 = Team(name="t2")
        dummy_t3 = Team(name="t3")
        dummy_t4 = Team(name="t4")
        dummy_p1 = Player(name="p1", team=dummy_t1, bracket=2, stars=2, preference=0, availability=15)
        dummy_p2 = Player(name="p2", team=dummy_t2, bracket=2, stars=2, preference=0, availability=15)
        dummy_p3 = Player(name="p3", team=dummy_t3, bracket=2, stars=2, preference=0, availability=15)
        dummy_p4 = Player(name="p4", team=dummy_t4, bracket=2, stars=2, preference=0, availability=15)
        dummy_ffa_match = FFaMatch(player1=dummy_p1, player2=dummy_p2, player3=dummy_p3, player4=dummy_p4, location="M", winner=dummy_p2)
        dummy_1v1_match = OvOMatch(player1=dummy_p1, player2=dummy_p2, location="M", winner=dummy_p2)
        return render(request, "matchmaking/detail.html", {"object_list":[dummy_ffa_match, dummy_1v1_match]})

    def post(self, request):
        return HttpResponse("how did this happen?")
