from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	return HttpResponse('Site under construction<br> <a href="https://github.com/Rhahi/MartianEnterpriseTournament/blob/master/design-document.txt"> Martian Enterprise Design Document </a><br>Sign up by posting in #martian-enterprise in <a href="https://discord.gg/0pQ0rgV4DDFxO2rD">the official discord server</a>')


def mainpage(request):
	return render(request, "main.html", {})

def testpage(request):
	return render(request, "test.html", {})

def rules(request):
	return render(request, "rules.html", {})

def player(request):
	return render(request, "player.html", {})

def schedule(request):
	return render(request, "schedule.html", {})
