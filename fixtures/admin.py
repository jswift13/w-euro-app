# fixtures/admin.py

from django.contrib import admin
from .models import Matchday, Team, Player, Match

@admin.register(Matchday)
class MatchdayAdmin(admin.ModelAdmin):
    list_display = ('order', 'name')
    ordering     = ('order',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display   = ('name', 'fifa_code')
    search_fields  = ('name', 'fifa_code')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display  = ('name', 'team', 'position')
    list_filter   = ('team', 'position')
    search_fields = ('name',)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display  = ('matchday', 'home', 'away', 'kickoff_time', 'venue', 'day_of_week')
    list_filter   = ('matchday', 'venue', 'day_of_week')
    ordering      = ('matchday', 'kickoff_time')
