"""Tasks for the celery."""
from celery import shared_task
from application_services import get_question_service

@shared_task(name="add_question")
def add_question():
    get_question_service().add_question(
        question_text="A very new question"
    )

    return "Question created successfully."
