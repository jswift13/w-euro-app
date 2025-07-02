import json
import requests

from django.core.management.base import BaseCommand, CommandError
from fixtures.models import Team, Player

class Command(BaseCommand):
    help = (
        "Import players from JSON or URL. "
        "Expects a list of objects {name, position, team_code}, "
        "or a top-level { 'players': [ … ] }"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'source',
            help='Filesystem path or HTTP URL to JSON list of players'
        )

    def handle(self, *args, **options):
        source = options['source']
        # 1. Load JSON payload
        try:
            if source.startswith(('http://', 'https://')):
                resp = requests.get(source)
                resp.raise_for_status()
                payload = resp.json()
            else:
                with open(source, encoding='utf-8') as f:
                    payload = json.load(f)
        except Exception as e:
            raise CommandError(f"Could not load JSON from {source!r}: {e}")

        # 2. Normalize to list of player dicts
        if isinstance(payload, dict) and 'players' in payload:
            players = payload['players']
        elif isinstance(payload, list):
            players = payload
        else:
            raise CommandError("JSON must be a list or contain a top-level 'players' key")

        # 3. Iterate and upsert
        for entry in players:
            name = entry.get('name', '').strip()
            position = entry.get('position', '').strip()
            code = entry.get('team_code', '').strip().upper()

            if not name or not position or not code:
                self.stdout.write(self.style.WARNING(
                    f"Skipping incomplete entry: {entry}"
                ))
                continue

            try:
                team = Team.objects.get(fifa_code=code)
            except Team.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"Skipping {name}: team code '{code}' not found"
                ))
                continue

            player, created = Player.objects.update_or_create(
                name=name,
                team=team,
                defaults={'position': position}
            )
            verb = 'Created' if created else 'Updated'
            self.stdout.write(f"{verb} player: {player.name} ({team.fifa_code})")

        self.stdout.write(self.style.SUCCESS("Players import complete."))
