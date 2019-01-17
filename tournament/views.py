
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
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
    def post(self, request, amount=2):
        # matchmaking method was designed with a different format in mind. let's convert to that format before
        # using it
        # TODO implement 1v1 matchmaking
        # TODO implement location choosing in matchmaking
        day = 1
        dawnplayers = {}
        db_players = Player.objects.all()
        if len(db_players)<4: return HttpResponse("Not enough players in the database to generate a match")
        for p in db_players:
            dmp = dc.Player(p.name, p.bracket, 0, p.team.id)
            dmp.availability = p.availability
            dmp.matches_played = len(p.get_matches())
            pref = []
            for i in range(3):
                pref.append(bool(p.preference&1<<i))
            dmp.preference = pref
            
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

        return HttpResponse("OK")
        return redirect('matchmaking-root')

        #return render(request, "matchmaking/matchmaking.html", {"object_list":result})



    def get(self, request):
        return HttpResponse("How did this happen?")


class RemoveMatch(DeleteView):
    model = FFaMatch


class MatchView(View):
    def get(self, request, match_id=None):

        if match_id:
            ans = get_object_or_404(FFaMatch, id=match_id);
        else:
            dummy_t1 = Team(name="Alpacas")
            dummy_t2 = Team(name="Beltalawda")
            dummy_t3 = Team(name="Circus")
            dummy_t4 = Team(name="Donkeys")
            dummy_p1 = Player(name="Asimov", team=dummy_t1, bracket=2, stars=2, preference=7, availability=15)
            dummy_p2 = Player(name="Bradbury", team=dummy_t2, bracket=2, stars=2, preference=7, availability=15)
            dummy_p3 = Player(name="Clarke", team=dummy_t3, bracket=2, stars=2, preference=7, availability=15)
            dummy_p4 = Player(name="Heinlein", team=dummy_t4, bracket=2, stars=2, preference=7, availability=15)
            dummy_ffa_match = FFaMatch(player1=dummy_p1, player2=dummy_p2, player3=dummy_p3, player4=dummy_p4, location="M", winner=dummy_p2)
            dummy_1v1_match = OvOMatch(player1=dummy_p1, player2=dummy_p2, location="M", winner=dummy_p2)
            ans = dummy_ffa_match
        return render(request, "matchmaking/detail.html", {"object_list": [ans]})

    def post(self, request):
        return HttpResponse("how did this happen?")