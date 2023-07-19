run:

		python manage.py runserver

start:

		gunicorn task_manager.wsgi

trans:

		python manage.py makemessages -l ru -i .venv

compile:

		python manage.py compilemessages

lint:

		poetry run flake8 task_manager