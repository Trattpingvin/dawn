from django.contrib import admin
from tournament.models import *


def publish_match(modeladmin, request, queryset):
	queryset.update(published=True)


publish_match.short_description = "Publish match on lineup page"


class MatchAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'published']
	ordering = ['-day', 'round']
	actions = [publish_match]


admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Match, MatchAdmin)
admin.site.register(Award)
admin.site.register(MatchResult)