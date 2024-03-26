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
    'debug_toolbar',
]

MIDDLEWARE += [
    'silk.middleware.SilkyMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

if os.environ.get('REPAIR_NINJA_DISABLE_DRF_INPUTS') == '1':
    REST_FRAMEWORK.update(
        {
            'DEFAULT_RENDERER_CLASSES': (
                'rest_framework.renderers.JSONRenderer',
                'repair_ninja.utils.BrowsableAPIRendererWithoutForms',  # Disable DRF's HTML Inputs
            ),
        }
    )

SIMPLE_JWT.update(
    {
        'ACCESS_TOKEN_LIFETIME': timedelta(days=31),
    }
)
