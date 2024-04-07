"""
Django base settings for Repair Ninja project.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'otp',
    'repair_core',
    'sms_message',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'repair_ninja.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'repair_ninja.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('REPAIR_NINJA_DB_ENGINE'),
        'NAME': os.environ.get('REPAIR_NINJA_DB_NAME'),
        'HOST': os.environ.get('REPAIR_NINJA_DB_HOST'),
        'PORT': os.environ.get('REPAIR_NINJA_DB_PORT'),
        'USER': os.environ.get('REPAIR_NINJA_DB_USER'),
        'PASSWORD': os.environ.get('REPAIR_NINJA_DB_PASSWORD')
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django rest framework settings
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Simple JWT settings
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
}

# Djoser settings
# https://djoser.readthedocs.io/en/latest/settings.html

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'repair_ninja.serializers.UserCreateSerializer',
        'current_user': 'repair_ninja.serializers.UserSerializer',
    },
    'PERMISSIONS': {
        # Overriding the set_password permission class is not really necessary.
        'set_password': ['repair_core.permissions.CurrentUserOrSuperUser'],
        'username_reset': ['repair_core.permissions.IsSuperUser'],
        'username_reset_confirm': ['repair_core.permissions.IsSuperUser'],
        'set_username': ['repair_core.permissions.IsSuperUser'],
        'user_create': ['rest_framework.permissions.IsAdminUser'],
        'user_delete': ['repair_core.permissions.IsSuperUser'],
    },
}

# SMS.ir settings
SMS_ENABLED = bool(int(os.environ.get('REPAIR_NINJA_SMS_ENABLED', 0)))
SMS_API_KEY = os.environ.get('REPAIR_NINJA_SMS_API_KEY')
SMS_LINE_NUMBER = os.environ.get('REPAIR_NINJA_SMS_LINE_NUMBER', 0)
