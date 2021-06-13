APP_LIST ?= main teachers

.PHONY: collectstatic run test ci migrations staticfiles

help:
	@echo "Available commands"
	@echo " - run 			: runs the development server"
	@echo " - shell			: runs the development shell"
	