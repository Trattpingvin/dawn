from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
	path('', TemplateView.as_view(template_name='main.html'), name='tournament-root'),
	path('martian-enterprise', TemplateView.as_view(template_name='main.html'), name='martian-enterprise'),
	path('martian-enterprise/rules', TemplateView.as_view(template_name='rules.html'), name="rules"),
	path('martian-enterprise/schedule', TemplateView.as_view(template_name='schedule/schedule.html'), name="schedule"),
	path('martian-enterprise/players', TemplateView.as_view(template_name='players.html'), name="players"),
	path('martian-enterprise/schedule/day1', views.DayView.as_view(template_name='schedule/day1.html', day = 1) , name='day1'),
	path('martian-enterprise/schedule/day2', views.DayView.as_view(template_name='schedule/day2.html', day = 2) , name='day2'),
	path('martian-enterprise/schedule/day3', views.DayView.as_view(template_name='schedule/day3.html', day = 3) , name='day3'),
	path('martian-enterprise/schedule/day4', views.DayView.as_view(template_name='schedule/day4.html', day = 4) , name='day4'),
	path('martian-enterprise/schedule/workshop', TemplateView.as_view(template_name='schedule/workshop.html'), name='workshop'),
	path('martian-enterprise/schedule/drafting', TemplateView.as_view(template_name='schedule/drafting.html'), name='drafting'),
]
urlpatterns += [
	path('matchmaking/', login_required(views.MainView.as_view()), name='matchmaking-root'),
    path('martian-enterprise/matchmaking/', login_required(views.MainView.as_view()), name='matchmaking-root'),
    path('martian-enterprise/matchmaking/genffa', login_required(views.GenMatchesView.as_view()), name='genffa'),
    path('martian-enterprise/matchmaking/genffa/<int:amount>', login_required(views.GenMatchesView.as_view()), name='genffa'),
    path('martian-enterprise/matchmaking/gen1v1', login_required(views.GenMatchesView.as_view()), name='gen1v1'),
    path('martian-enterprise/matchmaking/removematch/<int:match_id>', login_required(views.RemoveMatch.as_view()), name='removematch'),
    path('martian-enterprise/matchmaking/removematch/', login_required(views.RemoveMatch.as_view()), name='removematch'),
    path('martian-enterprise/matchmaking/inspectmatch/<int:match_id>', login_required(views.MatchView.as_view()), name='inspectmatch'),
    path('martian-enterprise/matchmaking/inspectmatch/', views.MatchView.as_view(), name='inspectmatch'),
]