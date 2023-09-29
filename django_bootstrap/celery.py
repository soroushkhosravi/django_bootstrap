import os

from celery import Celery
from datetime import datetime

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_bootstrap.settings')

app = Celery('django_bootstrap')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True, name="add_question")
def create_question(self):
    from application_services import get_question_service
    question_service = get_question_service().add_question(
        question_text="A question from inside the celery task."
    )
    return question_service.id