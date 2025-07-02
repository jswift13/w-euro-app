# fixtures/models.py

from django.db import models

class Matchday(models.Model):
    GROUP_MD1 = 'Group Stage – Matchday 1'
    GROUP_MD2 = 'Group Stage – Matchday 2'
    GROUP_MD3 = 'Group Stage – Matchday 3'
    QUARTER   = 'Quarter-finals'
    SEMI      = 'Semi-finals'
    FINAL     = 'Final'

    NAME_CHOICES = [
        (GROUP_MD1, 'Group Stage – Matchday 1'),
        (GROUP_MD2, 'Group Stage – Matchday 2'),
        (GROUP_MD3, 'Group Stage – Matchday 3'),
        (QUARTER,   'Quarter-finals'),
        (SEMI,      'Semi-finals'),
        (FINAL,     'Final'),
    ]

    name  = models.CharField(max_length=30, choices=NAME_CHOICES, unique=True)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Team(models.Model):
    name      = models.CharField(max_length=100)
    fifa_code = models.CharField(max_length=3, unique=True)
    flag_url  = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    name     = models.CharField(max_length=100)
    position = models.CharField(max_length=30)
    team     = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.team.fifa_code})"


class Match(models.Model):
    matchday     = models.ForeignKey(Matchday, on_delete=models.PROTECT, related_name='matches')
    home        = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away        = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    kickoff_time = models.DateTimeField()
    venue        = models.CharField(max_length=50)
    day_of_week   = models.CharField(max_length=50)
    score_home  = models.PositiveSmallIntegerField(null=True, blank=True)
    score_away  = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.home} vs {self.away} · {self.kickoff_time}"
    
    class Meta:
        verbose_name_plural = "Matches"
