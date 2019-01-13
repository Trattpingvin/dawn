from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='matchmaking-root'),
	path('genffa', views.gen_ffa_matches, name='genffa'),
	path('gen1v1', views.gen_1v1_matches, name='gen1v1'),
	path('removematch/<int:match_id>', views.remove_match, name='removematch'),
	path('removematch/', views.remove_match, name='removematch'),
	path('inspectmatch/<int:match_id>', views.inspect_match, name='inspectmatch'),
	path('inspectmatch/', views.inspect_match, name='inspectmatch'),
	path('showmatch/<int:match_id>', views.show_match, name='showmatch'),
	path('showmatch/', views.show_match, name='showmatch'),
]
