dev-docker:
	docker compose --file docker-compose.dev.yml up --build

dev:
	uv run python -m fastapi dev app/main.py --host 0.0.0.0 --port 8000

dev-migrate:
	alembic upgrade head

start:
	gunicorn \
			-k uvicorn.workers.UvicornWorker \
			-w 4 \
			-b 0.0.0.0:8000 \
			app.main:app
