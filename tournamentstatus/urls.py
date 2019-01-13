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
	path('day1', views.day1 , name='day1'),
	path('day2', views.day2 , name='day2'),
	path('day3', views.day3 , name='day3'),
	path('day4', views.day4 , name='day4'),
	path('workshop', views.workshop, name='workshop')
]
