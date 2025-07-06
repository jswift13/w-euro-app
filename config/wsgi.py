"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import environ
from django.core.wsgi import get_wsgi_application

# Build paths inside the project like this: BASE_DIR / ...
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# read .env file
env = environ.Env()
env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file):
    environ.Env.read_env(env_file)

# allow overriding via environment; default to prod settings
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    env('DJANGO_SETTINGS_MODULE', default='config.settings.prod')
)

application = get_wsgi_application()



