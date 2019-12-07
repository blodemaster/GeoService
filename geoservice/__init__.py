from celery import Celery
from flask import Flask

import config


def create_app():
    """Create a Flask application."""
    app = Flask(__name__)

    app.config.from_object(config)

    return app


def create_celery(app):
    """Create a Celery application"""
    celery = Celery(
        app.name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
