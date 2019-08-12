from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_var('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS += env_var('ALLOWED_HOSTS').split(',')

# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = env_var('EMAIL_HOST')
EMAIL_HOST_USER = env_var('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env_var('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env_var('EMAIL_PORT')
