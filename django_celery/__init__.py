from .celery import app as celery_app

__all__ = ("celery_app",)

@celery_app.task()
def add(a, b):
    return a + b