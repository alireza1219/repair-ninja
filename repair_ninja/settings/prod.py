"""
Django production settings for Repair Ninja project.

See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
"""

import os

from repair_ninja.settings.base import REST_FRAMEWORK

SECRET_KEY = os.environ.get('REPAIR_NINJA_DJANGO_SECRET_KEY')

STATIC_ROOT = '/vol/web/static'

DEBUG = False

ALLOWED_HOSTS = os.environ.get('REPAIR_NINJA_ALLOWED_HOSTS', '').split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get('REPAIR_NINJA_CSRF_TRUSTED_ORIGINS', '').split(',')

REST_FRAMEWORK.update(
    {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        ),
    }
)

if bool(int(os.environ.get('REPAIR_NINJA_SMTP'), 0)):
    EMAIL_HOST = os.environ.get('REPAIR_NINJA_EMAIL_HOST')
    EMAIL_PORT = os.environ.get('REPAIR_NINJA_EMAIL_PORT')
    EMAIL_USE_TLS = bool(int(os.environ.get('REPAIR_NINJA_EMAIL_USE_TLS', 1)))
    EMAIL_HOST_USER = os.environ.get('REPAIR_NINJA_EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('REPAIR_NINJA_EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = os.environ.get('REPAIR_NINJA_DEFAULT_FROM_EMAIL')
