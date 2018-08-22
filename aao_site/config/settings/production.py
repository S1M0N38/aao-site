from .base import *


DEBUG = False

ALLOWED_HOSTS += []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('NAME_DB'),
        'USER': get_env_variable('USER_DB'),
        'PASSWORD': get_env_variable('PASSWORD_DB'),
        'HOST': get_env_variable('HOST_DB'),
        'PORT': '',
    }
}
