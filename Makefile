APP_LIST ?= main teachers

.PHONY: collectstatic run test ci migrations staticfiles

help:
	@echo "Available commands"
	@echo " - run	 			: runs the development server"
	@echo " - shellplus			: runs the development shell"
	@echo " - install			: installs production requirements"
	@echo " - install-dev			: installs development requirements"
	@echo " - setup-test-data		: erases the db and loads mock data"

run:
	python manage.py runserver

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