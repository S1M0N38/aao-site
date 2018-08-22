from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "SecretKeyForUseOnTravis"

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'travisci',
        'USER':     'postgres',
        'PASSWORD': '',
        'HOST':     'localhost',
        'PORT':     '',
    }
}
