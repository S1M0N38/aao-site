from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_var('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS += ['127.0.0.1', '0.0.0.0']
