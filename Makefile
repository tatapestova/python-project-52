run:

		python manage.py runserver

start:

		gunicorn task_manager.wsgi

install:

		poetry install

migrate:

		poetry run python manage.py makemigrations
		poetry run python manage.py migrate


trans:

		python manage.py makemessages -l ru -i .venv

compile:

		python manage.py compilemessages

lint:

		poetry run flake8 task_manager

test:

		poetry run python3 manage.py test

test-coverage:
	
		poetry run coverage run manage.py test
		poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
		poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py
