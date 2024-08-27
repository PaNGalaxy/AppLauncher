service nginx restart
poetry run python manage.py migrate
poetry run python -m gunicorn launcher_app.asgi:application -k uvicorn.workers.UvicornWorker --workers=1
