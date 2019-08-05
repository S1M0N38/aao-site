from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS += get_env_variable('ALLOWED_HOSTS').split(',')
