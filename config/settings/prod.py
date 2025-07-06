# config/settings/prod.py

import os
from .base import *

# ----------------------
# SECURITY & ENV
# ----------------------

DEBUG = False

# Pull SECRET_KEY from env; fail loudly if it’s missing
SECRET_KEY = env('SECRET_KEY')

# Your Render service URL (or comma-separated list)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['your-app-name.onrender.com'])

# ----------------------
# DATABASE
# ----------------------

# Render provides DATABASE_URL in its env
db_url = env('DATABASE_URL', default=None)
if db_url:
    DATABASES['default'] = env.db_url('DATABASE_URL')

# ----------------------
# STATIC FILES (WhiteNoise)
# ----------------------

# Where `collectstatic` will gather your assets
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Tell Django to use WhiteNoise’s compressed, manifest-based storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Inject Whitenoise middleware right after SecurityMiddleware
# (so it can intercept requests for static files)
MIDDLEWARE.insert(
    MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1,
    'whitenoise.middleware.WhiteNoiseMiddleware',
)

# ----------------------
# OPTIONAL: S3 FILE STORAGE
# (if/when you add django-storages[boto3])
# ----------------------
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_ACCESS_KEY_ID        = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY    = env('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME  = env('AWS_STORAGE_BUCKET_NAME')
