from django.shortcuts import render
from django.http import HttpResponse

from dawnotc import classes



def index(request):
	player = classes.Player("name")
	return HttpResponse(str(player))
	return HttpResponse("Hello. I am an offworld matchmaker.")
