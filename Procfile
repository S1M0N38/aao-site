release: pipenv run python aao_site/manage.py migrate --noinput
web: gunicorn aao_site.config.wsgi
