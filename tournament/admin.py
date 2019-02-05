from django.contrib import admin
from tournament.models import *
from django.utils.html import format_html
from django.urls import reverse

def publish_match(modeladmin, request, queryset):
	queryset.update(published=True)


def score_match(match):
	if match.result:
		return "Already Scored"
	return format_html('<a href="{}">{}</a>', reverse('scorematch')+str(match.id), "Score match")


publish_match.short_description = "Publish match on lineup page"
score_match.short_description = "Score match"


class MatchAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'published', score_match]
	ordering = ['-day', 'round']
	actions = [publish_match]


admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Match, MatchAdmin)
admin.site.register(Award)
admin.site.register(MatchResult)