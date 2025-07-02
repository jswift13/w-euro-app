# predictions/admin.py

from django.contrib import admin
from .models import Prediction, MatchPick

class MatchPickInline(admin.TabularInline):
    model = MatchPick
    extra = 0


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display  = ('matchday', 'favorite_team', 'potm', 'submitted_at')
    list_filter   = ('matchday', 'favorite_team')
    date_hierarchy = 'submitted_at'
    inlines       = (MatchPickInline,)
