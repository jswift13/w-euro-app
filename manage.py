#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys
import environ

def main():
    """Run administrative tasks."""
    # 1) Load environment variables from .env (if present)
    env = environ.Env()
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        environ.Env.read_env(env_file)

    # 2) Default to production settings, unless overridden in the env
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        env('DJANGO_SETTINGS_MODULE', default='config.settings.prod')
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django – make sure your virtualenv is activated "
            "and django is installed."
        ) from exc

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

