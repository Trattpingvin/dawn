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

def players(request):
	return render(request, "players.html", {})

def schedule(request):
	return render(request, "schedule.html", {})

def day1(request):
	return render(request, "schedule/day1.html", {})

def day2(request):
	return render(request, "schedule/day2.html", {})

def day3(request):
	return render(request, "schedule/day3.html", {})

def day4(request):
	return render(request, "schedule/day4.html", {})

def workshop(request):
	return render(request, "schedule/workshop.html", {})

def drafting(request):
	return render(request, "schedule/drafting.html", {})