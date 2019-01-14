from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
	path('', login_required(views.MainView.as_view()), name='matchmaking-root'),
	path('genffa', login_required(views.GenMatchesView.as_view()), name='genffa'),
	path('gen1v1', login_required(views.GenMatchesView.as_view()), name='gen1v1'),
	path('removematch/<int:match_id>', login_required(views.RemoveMatch.as_view()), name='removematch'),
	path('removematch/', login_required(views.RemoveMatch.as_view()), name='removematch'),
	path('inspectmatch/<int:match_id>', login_required(views.MatchView.as_view()), name='inspectmatch'),
	path('inspectmatch/', login_required(views.MatchView.as_view()), name='inspectmatch'),
]
