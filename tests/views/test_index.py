"""Tests related to the index view."""
import pytest
from django.test import Client
from polls.models import Question
from datetime import datetime


@pytest.mark.django_db(reset_sequences=True)
def test_index_view():
    """We can test the index view."""
    client = Client()

    response = client.get('/polls/')

    assert response.status_code == 200
    assert response.json() == {"message": "successful."}


@pytest.mark.django_db(reset_sequences=True)
def test_get_question_for_invalid_id():
    """Tests getting a question."""
    client = Client()

    response = client.get('/polls/1')

    assert response.status_code == 400
    assert response.content == b'Question not found.'


@pytest.mark.django_db(reset_sequences=True)
def test_get_question_for_valid_id():
    """Tests getting a question."""
    Question.objects.create(
        question_text="First question.",
        pub_date=datetime.now()
    )
    client = Client()

    response = client.get('/polls/1')

    assert response.status_code == 200
    assert response.json() == {'message': 'successful.'}

