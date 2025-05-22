PROJECT_DIR := src
MANAGE := python $(PROJECT_DIR)/manage.py
FIXTURE_PATH := main/fixtures/fixt_cv.json

run:
	$(MANAGE) runserver 0.0.0.0:8000

docker_run:
	docker-compose up --build

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

load_data:
	$(MANAGE) loaddata cv_fixture

docker_load_data:
	docker compose exec web $(MANAGE) loaddata cv_fixture

remove_data:
	$(MANAGE) flush

docker_remove_data:
	docker compose exec web $(MANAGE) flush

run_tests:
	$(MANAGE) test main.tests api.tests audit.tests
