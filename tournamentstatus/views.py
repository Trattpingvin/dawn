from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from matchmaking.models import FFaMatch, OvOMatch
# Create your views here.

class DayView(TemplateView):
    day = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["FFA"] = FFaMatch.objects.filter(day = self.day)
        context["1v1"] = OvOMatch.objects.filter(day = self.day)

        return context