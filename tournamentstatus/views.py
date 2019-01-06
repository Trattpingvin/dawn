from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	return HttpResponse('Site under construction<br> <a href="https://github.com/Rhahi/MartianEnterpriseTournament/blob/master/design-document.txt"> Martian Enterprise Design Document </a>')
