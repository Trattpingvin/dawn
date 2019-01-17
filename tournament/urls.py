from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from . import views

matchmaking = [
    path('', login_required(views.MainView.as_view()), name='matchmaking-root'),
    path('genffa', login_required(views.GenMatchesView.as_view()), name='genffa'),
    path('genffa/<int:amount>', login_required(views.GenMatchesView.as_view()), name='genffa'),
    path('gen1v1', login_required(views.GenMatchesView.as_view()), name='gen1v1'),
    path('removematch/<int:match_id>', login_required(views.RemoveMatch.as_view()), name='removematch'),
    path('removematch/', login_required(views.RemoveMatch.as_view()), name='removematch'),
    path('inspectmatch/<int:match_id>', login_required(views.MatchView.as_view()), name='inspectmatch'),
    path('inspectmatch/', views.MatchView.as_view(), name='inspectmatch'),
]

martian_enterprise = [
    path('', TemplateView.as_view(template_name='main.html'), name='martian-enterprise'),
    path('matchmaking/', include(matchmaking)),
    path('rules', TemplateView.as_view(template_name='rules.html'), name="rules"),
    path('schedule', TemplateView.as_view(template_name='schedule/schedule.html'), name="schedule"),
    path('players', views.PlayersView.as_view(), name="players"),
    path('inspectplayer', views.PlayerView.as_view(), name="inspectplayer"),
    path('inspectplayer/<str:player_name>', views.PlayerView.as_view(), name="inspectplayer"),
    path('schedule/day1', views.DayView.as_view(template_name='schedule/day1.html', day = 1) , name='day1'),
    path('schedule/day2', views.DayView.as_view(template_name='schedule/day2.html', day = 2) , name='day2'),
    path('schedule/day3', views.DayView.as_view(template_name='schedule/day3.html', day = 3) , name='day3'),
    path('schedule/day4', views.DayView.as_view(template_name='schedule/day4.html', day = 4) , name='day4'),
    path('schedule/workshop', TemplateView.as_view(template_name='schedule/workshop.html'), name='workshop'),
    path('schedule/drafting', TemplateView.as_view(template_name='schedule/drafting.html'), name='drafting'),
]

urlpatterns = [
    path('', TemplateView.as_view(template_name='main.html'), name='tournament-root'),
    path('martian-enterprise/', include(martian_enterprise)),
    path('matchmaking/', include(matchmaking)),

]
