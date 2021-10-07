build:
	docker-compose up --build -d

makemigrations:
	docker-compose exec web alembic upgrade head

down:
	docker-compose down

clear:
	docker system prune -fa