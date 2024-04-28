"""
Django development settings for Repair Ninja project.
"""

import os

from datetime import timedelta

from repair_ninja.settings.base import INSTALLED_APPS, MIDDLEWARE, REST_FRAMEWORK, SIMPLE_JWT

SECRET_KEY = 'django-insecure-sfrd4)1bi+lh*uk-!)u8-7#p^q$#v0d+8=5dtrr%ww0fs(i*wr'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    'silk',
    'corsheaders',
    'debug_toolbar',
]

MIDDLEWARE += [
    'silk.middleware.SilkyMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [
    'http://localhost:5173'
]

if bool(int(os.environ.get('REPAIR_NINJA_DISABLE_DRF_INPUTS', 0))):
    REST_FRAMEWORK.update(
        {
            'DEFAULT_RENDERER_CLASSES': (
                'rest_framework.renderers.JSONRenderer',
                'repair_ninja.utils.BrowsableAPIRendererWithoutForms',  # Disable DRF's HTML Inputs.
            ),
        }
    )

# Fix Django Debug Toolbar not appearing when using Docker Compose.
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG
}

SIMPLE_JWT.update(
    {
        'ACCESS_TOKEN_LIFETIME': timedelta(days=31),
    }
)

# Set the `REPAIR_NINJA_EMAIL_HOST` environment variable to `localhost`
# if you are not running the project using Docker Compose.
EMAIL_HOST = os.environ.get('REPAIR_NINJA_EMAIL_HOST', 'smtp4dev')
