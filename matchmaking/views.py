from django.shortcuts import render
from django.http import HttpResponse
import sys
from django.contrib.admin.views.decorators import staff_member_required
from matchmaking.models import *
import dawnotc.matchmaking


@staff_member_required
def index(request):
	matches = FFaMatch.objects.all()
	return render(request, "matchmaking.html", {"matchlist":matches})

@staff_member_required
def gen_ffa_matches(request):
	amount = 5
	all_players = Player.objects.all()
	result = dawnotc.matchmaking.generate_matches(players)
	return render(request, "matchmaking.html", {"matchlist":result})

@staff_member_required
def gen_1v1_matches(request):
	pass

@staff_member_required
def remove_match(request, match_id = None):
	if not match_id:
		return HttpResponse("no match given")

@staff_member_required
def show_match(request, match_id = None):
	if not match_id:
		return HttpResponse("no match given")

@staff_member_required
def inspect_match(request, match_id=None):
	#POST view
	if not match_id:
		return HttpResponse("no match given")
	result = FFaMatch.objects.filter(id=match_id)
	if result: return HttpResponse(result[0])
	else: return HttpResponse("Error")
