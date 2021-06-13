APP_LIST ?= main teachers

.PHONY: collectstatic run test ci migrations staticfiles

help:
	@echo "Available commands"
	@echo " - run	 			: runs the development server"
	@echo " - shell			: runs the development server"
	@echo " - install			: installs production requirements"
	@echo " - install-dev			: installs development requirements"

run:
	python manage.py runserver

shell:
	python manage.py shell

install:
	python -m pip install -r requirements/base.txt

install-dev: install
	python -m pip install -r requirements/dev.txt
	python -m pip install -r requirements/test.txt