from django.contrib import admin
from tournament.models import *
#  TODO: add action to matches to publish them
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Award)
admin.site.register(MatchResult)
