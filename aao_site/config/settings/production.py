from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_var('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS += env_var('ALLOWED_HOSTS').split(',')
