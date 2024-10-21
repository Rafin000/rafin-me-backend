HOST ?= 0.0.0.0
PORT ?= 6000
TAG ?= 0.1

dev:
	FLASK_ENV=development poetry run python manage.py run -p $(PORT) -h $(HOST)

prod:
	gunicorn manage:app -w 4 --log-level INFO --bind $(HOST):$(PORT)

image:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	docker build -f Dockerfile -t rafin1998/rafin-blog-site:$(TAG) . || true
	rm requirements.txt

