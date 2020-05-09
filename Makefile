
build:
	docker-compose build

up:
	docker-compose up courses_platform

down:
	docker-compose down --remove-orphans

seed-db:
	docker-compose exec courses_platform python manage.py seed-db

test:
	docker-compose run --rm --no-deps --entrypoint=pytest courses_platform /home/courses_platform/tests/
