"""Covers the tests related to celery tasks."""
from polls.tasks import add_question
from polls.models import Question
import pytest


@pytest.mark.django_db(reset_sequences=True)
def test_add_question_adds_model_to_db():
    questions = Question.objects.all()

    assert len(questions) == 0

    response = add_question.apply(args=())

    assert response.status == 'SUCCESS'
    assert response.result == 'Question created successfully.'
    questions = Question.objects.all()

    assert len(questions) == 1
