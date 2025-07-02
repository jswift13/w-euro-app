# fixtures/management/commands/import_teams.py

import json
import requests

from django.core.management.base import BaseCommand, CommandError
from fixtures.models import Team

class Command(BaseCommand):
    help = 'Import teams from JSON or URL: expects list of {name, fifa_code, flag_url}.'

    def add_arguments(self, parser):
        parser.add_argument(
            'source',
            help='Filesystem path or HTTP URL to JSON list of teams'
        )

    def handle(self, *args, **options):
        source = options['source']
        # 1. Load JSON
        try:
            if source.startswith(('http://','https://')):
                resp = requests.get(source)
                resp.raise_for_status()
                teams = resp.json()
            else:
                with open(source, encoding='utf-8') as f:
                    teams = json.load(f)
        except Exception as e:
            raise CommandError(f"Could not load teams JSON from {source!r}: {e}")

        # 2. Validate
        if not isinstance(teams, list):
            raise CommandError("JSON payload must be a list of team objects")

        # 3. Upsert
        for entry in teams:
            code = entry.get('fifa_code', '').strip().upper()
            name = entry.get('name', '').strip()
            flag = entry.get('flag_url', '').strip()

            if not (code and name):
                self.stdout.write(self.style.WARNING(
                    f"Skipping invalid entry (missing name or code): {entry}"
                ))
                continue

            team, created = Team.objects.update_or_create(
                fifa_code=code,
                defaults={
                    'name': name,
                    'flag_url': flag,
                }
            )
            verb = 'Created' if created else 'Updated'
            self.stdout.write(f"{verb} team: {team.name} ({team.fifa_code})")

        self.stdout.write(self.style.SUCCESS("Teams import complete."))
