from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='tournamentstatus-root'),
	path('martian-enterprise', views.index, name='martian-enterprise'),
	path('test', views.mainpage, name="mainpage"),
	path('test2', views.testpage, name="testpage"),
	path('martian-enterprise/rules', views.rules, name="rules"),
	path('martian-enterprise/schedule', views.schedule, name="schedule"),
	path('martian-enterprise/players', views.players, name="players"),
	path('martian-enterprise/schedule/day1', views.day1 , name='day1'),
	path('martian-enterprise/schedule/day2', views.day2 , name='day2'),
	path('martian-enterprise/schedule/day3', views.day3 , name='day3'),
	path('martian-enterprise/schedule/day4', views.day4 , name='day4'),
	path('martian-enterprise/schedule/workshop', views.workshop, name='workshop'),
	path('martian-enterprise/schedule/drafting', views.drafting, name='drafting'),
]
