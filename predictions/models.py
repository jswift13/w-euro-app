# predictions/models.py

from django.db import models
from fixtures.models import Matchday, Match, Team, Player

class Prediction(models.Model):
    matchday      = models.ForeignKey(Matchday, on_delete=models.CASCADE, related_name='predictions')
    session_key   = models.CharField(max_length=40,default='', blank=True, db_index=True, help_text="Django session key to enforce one prediction per session")
    submitted_at  = models.DateTimeField(auto_now_add=True)
    favorite_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='favored_by')
    potm = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, verbose_name="Player of the Matchday")

    class Meta:
        unique_together = ('matchday', 'session_key')

    def __str__(self):
        return f"Prediction for {self.matchday} by session {self.session_key}"


class MatchPick(models.Model):
    prediction  = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name='picks')
    match       = models.ForeignKey(Match, on_delete=models.CASCADE)
    predicted_home_score = models.PositiveSmallIntegerField()
    predicted_away_score = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('prediction', 'match')

    def __str__(self):
            # Use match.home.name and match.away.name explicitly
            home = self.match.home.name
            away = self.match.away.name
            return f"{home} vs {away}: {self.predicted_home_score}–{self.predicted_away_score}"