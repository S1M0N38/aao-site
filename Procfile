release: pipenv run python aao_site/manage.py migrate --noinput
web: cd aao_site && gunicorn config.wsgi
