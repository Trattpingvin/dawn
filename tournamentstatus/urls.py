from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('martian-enterprise', views.index, name='index'),
	path('test', views.mainpage, name="mainpage"),
	path('test2', views.testpage, name="testpage"),
	path('rules', views.rules, name="rules"),
	path('schedule', views.schedule, name="schedule"),
	path('players', views.players, name="players"),
]
