from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS += get_env_variable('ALLOWED_HOSTS').split(',')

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
