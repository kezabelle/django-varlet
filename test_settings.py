# -*- coding: utf-8 -*-
import logging
import os

try:
    logging.getLogger('varlet').addHandler(logging.NullHandler())
except AttributeError:  # < Python 2.7
    pass


DEBUG = os.environ.get('DEBUG', 'on') == 'on'
SECRET_KEY = os.environ.get('SECRET_KEY', 'TESTTESTTESTTESTTESTTESTTESTTEST')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,testserver').split(',')
BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.admin',
    'varlet',
    'rest_framework',
]

SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False

STATIC_URL = '/__static__/'
MEDIA_URL = '/__media__/'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True


ROOT_URLCONF = 'test_urls'

# Use a fast hasher to speed up tests.
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

SITE_ID = 1

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

STATIC_ROOT = os.path.join(BASE_DIR, 'test_collectstatic')
MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')

TEMPLATE_DIRS = (
    os.path.realpath(
        os.path.join(BASE_DIR, 'varlet', 'tests', 'test_templates')
    ),
)

TEMPLATEFINDER_DISPLAY_NAMES = {
    "varlet/pages/layouts/a.html": "Template: a",
    "varlet/pages/layouts/b.html": "Another template: b",
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'COMPACT_JSON': False,
    'PAGE_SIZE': 10,
}

SILENCED_SYSTEM_CHECKS = [
    "1_7.W001",
    "varlet.W1",
]

USE_TZ = True
