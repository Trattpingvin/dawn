from django.urls import path
from django.views.generic.base import TemplateView

from . import views
TemplateView.as_view(template_name='')
urlpatterns = [
	path('', TemplateView.as_view(template_name='main.html'), name='tournamentstatus-root'),
	path('martian-enterprise', TemplateView.as_view(template_name='main.html'), name='martian-enterprise'),
	path('martian-enterprise/rules', TemplateView.as_view(template_name='rules.html'), name="rules"),
	path('martian-enterprise/schedule', TemplateView.as_view(template_name='schedule/schedule.html'), name="schedule"),
	path('martian-enterprise/players', TemplateView.as_view(template_name='players.html'), name="players"),
	path('martian-enterprise/schedule/day1', TemplateView.as_view(template_name='schedule/day1.html') , name='day1'),
	path('martian-enterprise/schedule/day2', TemplateView.as_view(template_name='schedule/day2.html') , name='day2'),
	path('martian-enterprise/schedule/day3', TemplateView.as_view(template_name='schedule/day3.html') , name='day3'),
	path('martian-enterprise/schedule/day4', TemplateView.as_view(template_name='schedule/day4.html') , name='day4'),
	path('martian-enterprise/schedule/workshop', TemplateView.as_view(template_name='schedule/workshop.html'), name='workshop'),
	path('martian-enterprise/schedule/drafting', TemplateView.as_view(template_name='schedule/drafting.html'), name='drafting'),
]
