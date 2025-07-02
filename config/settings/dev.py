# config/settings/dev.py

from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# In dev, use the SQLite URL from .env (or fallback)
DATABASES['default'] = env.db(default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'))

