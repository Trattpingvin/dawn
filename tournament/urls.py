from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from . import views

matchmaking = [
    path('', login_required(views.MatchStagingView.as_view()), name='matchmaking-root'),
    path('<int:day>', login_required(views.MatchStagingView.as_view()), name='matchmaking-root'),
    path('removematch/<int:match_id>', login_required(views.RemoveMatchView.as_view()), name='removematch'),
    path('removematch/', login_required(views.RemoveMatchView.as_view()), name='removematch'),
    path('scorematch/<int:match_id>', login_required(views.ScoreMatchView.as_view()), name='scorematch'),
    path('scorematch/', login_required(views.ScoreMatchView.as_view()), name='scorematch'),
    path('inspectmatch/<int:match_id>/<int:rnd>', views.MatchView.as_view(), name='inspectmatch'),
    path('inspectmatch/<int:match_id>', views.MatchView.as_view(), name='inspectmatch'),
    path('inspectmatch/', views.MatchView.as_view(), name='inspectmatch'),
]

martian_enterprise = [
    path('', TemplateView.as_view(template_name='main.html'), name='martian-enterprise'),
    path('matchmaking/', include(matchmaking)),
    path('rules', TemplateView.as_view(template_name='rules.html'), name="rules"),
    path('schedule', TemplateView.as_view(template_name='schedule/schedule.html'), name="schedule"),
    path('players', views.PlayersView.as_view(), name="players"),
    path('inspectplayer', views.PlayerView.as_view(), name="inspectplayer"),
    path('inspectplayer/<int:player_id>', views.PlayerView.as_view(), name="inspectplayer"),
    path('schedule/day', views.DayView.as_view(), name='day'),
    path('schedule/day/<int:day>', views.DayView.as_view(), name='day'),
    path('schedule/day/<int:day>/<int:start_match>', views.DayView.as_view(), name='day'),
    path('schedule/workshop', TemplateView.as_view(template_name='schedule/workshop.html'), name='workshop'),
    path('schedule/drafting', TemplateView.as_view(template_name='schedule/drafting.html'), name='drafting'),
]

urlpatterns = [
    path('', TemplateView.as_view(template_name='main.html'), name='tournament-root'),
    path('martian-enterprise/', include(martian_enterprise)),
    path('matchmaking/', include(matchmaking)),

]
