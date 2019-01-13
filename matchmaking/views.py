from django.shortcuts import render
from django.http import HttpResponse
import sys



def index(request):

	#return HttpResponse("<br>".join([a for a in sys.path]))
	import dawnotc.classes as dawn
	player = dawn.Player("name")
	return HttpResponse(str(player))
	return HttpResponse("Hello. I am an offworld matchmaker.")

def gen_ffa_matches(request):
	pass

def gen_1v1_matches(request):
	pass

def remove_match():
	pass
