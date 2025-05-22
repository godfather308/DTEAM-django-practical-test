PROJECT_DIR := src
MANAGE := python $(PROJECT_DIR)/manage.py
FIXTURE_PATH := main/fixtures/fixt_cv.json

run:
	$(MANAGE) runserver

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

load_data:
	$(MANAGE) loaddata $(PROJECT_DIR)/main/fixtures/cv_fixture.json

remove_data:
	$(MANAGE) flush

run_tests:
	$(MANAGE) test main.tests api.tests
