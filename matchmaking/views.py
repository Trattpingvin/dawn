from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
import sys
from django.contrib.admin.views.decorators import staff_member_required
from matchmaking.models import *
from django.views.generic import ListView, DeleteView
import dawnotc.matchmaking


class MainView(ListView):
	model = FFaMatch

class GenMatchesView(View):
	def post():
		amount = 5
		all_players = Player.objects.all()
		result = dawnotc.matchmaking.generate_matches(players)
		return render(request, "matchmaking.html", {"matchlist":result})

	def get():
		return HttpResponse("How did this happen?")

class RemoveMatch(DeleteView):
	model = FFaMatch

class MatchView(View):
	def get():
		dummy_t1 = Team(name="t1")
		dummy_t2 = Team(name="t2")
		dummy_t3 = Team(name="t3")
		dummy_t4 = Team(name="t4")
		dummy_p1 = Player(name="p1", team=dummy_t1, bracket=2, stars=2, preference=0, availability=15)
		dummy_p2 = Player(name="p2", team=dummy_t2, bracket=2, stars=2, preference=0, availability=15)
		dummy_p3 = Player(name="p3", team=dummy_t3, bracket=2, stars=2, preference=0, availability=15)
		dummy_p4 = Player(name="p4", team=dummy_t4, bracket=2, stars=2, preference=0, availability=15)
		dummy_match = Match(player1=dummy_p1, player2=dummy_p2, player3=dummy_p3, player4=dummy_p4, location="M", winner=dummy_p2)

		return render(request, "matchmaking.html", {"matchlist":[dummy_match]})

	def post():
		if not match_id:
			return HttpResponse("no match given")
		result = FFaMatch.objects.filter(id=match_id)
		if result: return HttpResponse(result[0])
		else: return HttpResponse("Error")
