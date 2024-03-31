"""
Django production settings for Repair Ninja project.

See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
"""

import os

from repair_ninja.settings.base import REST_FRAMEWORK

SECRET_KEY = os.environ.get('REPAIR_NINJA_DJANGO_SECRET_KEY')

STATIC_ROOT = '/vol/web/static'

DEBUG = False

ALLOWED_HOSTS = ['.alireza1219.ir']

CSRF_TRUSTED_ORIGINS = ['https://*.alireza1219.ir']

REST_FRAMEWORK.update(
    {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
    }
)
