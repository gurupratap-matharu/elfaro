APP_LIST ?= main classroom users

.PHONY: collectstatic run test ci install install-dev migrations staticfiles

help:
	@echo "Available commands"
	@echo " - run	 			: runs the development server"
	@echo " - ci	 			: lints, checks migrations, runs tests and show coverage report"
	@echo " - shellplus			: runs the development shell"
	@echo " - install			: installs production requirements"
	@echo " - install-dev			: installs development requirements"
	@echo " - setup-test-data		: erases the db and loads mock data"
	@echo " - isort			: sorts all imports of the project"
	@echo " - lint				: lints the codebase"

collectstatic:
	python manage.py collectstatic --noinput

clean:
	rm -rf __pycache__ .pytest_cache

migrations-check:
	python manage.py makemigrations --check --dry-run

test: migrations-check
	@coverage run --source=. manage.py test -v 2 $(APP_LIST)

ci: lint test
	python manage.py coverage report

isort:
	isort $(APP_LIST)

isort-check:
	isort -c $(APP_LIST)

lint: isort
	pylint $(APP_LIST)

check:
	python manage.py check

check-deploy:
	python manage.py check --deploy

run:
	python manage.py runserver 0.0.0.0:8000

shell:
	python manage.py shell

shellplus:
	python manage.py shell_plus

install:
	python -m pip install -r requirements/base.txt

install-dev: install
	python -m pip install -r requirements/dev.txt
	python -m pip install -r requirements/test.txt

setup-test-data:
	python manage.py setup_test_data