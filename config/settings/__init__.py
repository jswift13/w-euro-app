import os

ENV = os.getenv('DJANGO_ENV', 'dev').lower()

if ENV == 'prod':
    from .prod import *
else:
    from .dev import *


# if DJANGO_SETTINGS_MODULE not set, fall back to dev:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')