# fixtures/management/commands/import_fixtures.py

import json
import requests
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from fixtures.models import Team, Matchday, Match

# Map numeric matchday → your choice string
MD_NAME = {
    1: 'Group Stage – Matchday 1',
    2: 'Group Stage – Matchday 2',
    3: 'Group Stage – Matchday 3',
    4: 'Quarter-finals',
    5: 'Semi-finals',
    6: 'Final',
}

class Command(BaseCommand):
    help = 'Import matchday fixtures from JSON or URL'

    def add_arguments(self, parser):
        parser.add_argument(
            'source',
            help='Path or URL to JSON list of fixtures'
        )

    def handle(self, *args, **options):
        source = options['source']
        # 1. Load and parse JSON
        try:
            if source.startswith(('http://','https://')):
                resp = requests.get(source)
                resp.raise_for_status()
                records = resp.json()
            else:
                with open(source, encoding='utf-8') as f:
                    records = json.load(f)
        except Exception as e:
            raise CommandError(f"Failed to load fixtures JSON: {e}")

        if not isinstance(records, list):
            raise CommandError("Expected JSON list of fixture records")

        # 2. Iterate & upsert
        for rec in records:
            # a) Normalize types
            md_raw = rec.get('Matchday') or rec.get('matchday')
            try:
                md_num = int(md_raw)
            except Exception:
                self.stdout.write(self.style.WARNING(
                    f"Invalid Matchday number {md_raw!r}, skipping."
                ))
                continue

            md_name = MD_NAME.get(md_num)
            if not md_name:
                self.stdout.write(self.style.ERROR(
                    f"No mapping for Matchday {md_num}, skipping."
                ))
                continue

            # b) Get or create the Matchday bucket
            matchday, _ = Matchday.objects.get_or_create(
                name=md_name,
                defaults={'order': md_num}
            )

            # c) Parse kickoff datetime
            date_s = rec.get('Date')   # "2025-07-02"
            time_s = rec.get('Time')   # "18:00"
            if not date_s or not time_s:
                self.stdout.write(self.style.WARNING(
                    f"Missing Date/Time in record {rec}"
                ))
                continue

            try:
                naive = datetime.fromisoformat(f"{date_s}T{time_s}")
                kickoff = timezone.make_aware(naive, timezone.get_current_timezone())
            except Exception:
                self.stdout.write(self.style.WARNING(
                    f"Invalid Date/Time format {date_s} {time_s}, skipping."
                ))
                continue

            # d) Lookup teams by name (or you could add codes in your notebook)
            home_name = rec.get('Home') or rec.get('home')
            away_name = rec.get('Away') or rec.get('away')
            try:
                home = Team.objects.get(name__iexact=home_name.strip())
                away = Team.objects.get(name__iexact=away_name.strip())
            except Team.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"Unknown team in record: Home={home_name}, Away={away_name}"
                ))
                continue

            # e) Day-of-week and venue
            day = rec.get('Day') or rec.get('day_of_week') or ''
            venue = rec.get('Venue') or rec.get('venue') or ''

            # f) Upsert Match
            match, created = Match.objects.update_or_create(
                matchday=matchday,
                home=home,
                away=away,
                kickoff_time=kickoff,
                defaults={
                    'day_of_week': day,
                    'venue':       venue.strip(),
                }
            )
            verb = 'Created' if created else 'Updated'
            self.stdout.write(f"{verb} {home.name} vs {away.name} @ {kickoff}")

        self.stdout.write(self.style.SUCCESS("Fixtures import complete."))
