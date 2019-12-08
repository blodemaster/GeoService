import logging
import os

PROJECT_NAME = "geoservice"

# flask app
DEBUG = os.environ.get('DEBUG', False)
LOGGER_NAME = f"{PROJECT_NAME}_log"
LOG_FILENAME = os.environ.get("LOG_PATH", f"/var/tmp/app.{PROJECT_NAME}.log")
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOG_FORMAT = "%(asctime)s %(levelname)s\t: %(message)s"

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

# Celery settings
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 5
