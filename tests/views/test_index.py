"""Tests related to the index view."""
import pytest
from django.test import Client
from polls.models import Question, Choice
from datetime import datetime
from freezegun import freeze_time
import json


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

    response = client.get('/polls/question/1')

    assert response.status_code == 400
    assert response.json() == {'message': 'Question not found.', 'status': 'error'}


@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_get_question_for_valid_id():
    """Tests getting a question."""
    question = Question.objects.create(
        question_text="First question.",
        pub_date=datetime.now()
    )

    Choice.objects.create(question=question, choice_text="Choice 1", votes=10)

    client = Client()

    response = client.get('/polls/question/1')

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'question_text': 'First question.',
        'pub_date': '2020-10-10T00:00:00Z',
        'choices': [{'choice_text': 'Choice 1', 'id': 1, 'votes': 10}]
    }


@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_updated_for_valid_data():
    """Tests getting a question."""
    question = Question.objects.create(
        question_text="First question.",
        pub_date=datetime.now()
    )

    Choice.objects.create(question=question, choice_text="Choice 1", votes=10)

    client = Client()

    valid_data = {
            "question_text": "changed",
            "pub_date": "2020-10-15",
            "choices": [
                {
                    "id": 1,
                    "choice_text": "choice 1 changed"
                },
                {
                    "choice_text": "new choice"
                }
            ]
        }

    response = client.put('/polls/question/1', json.dumps(valid_data))

    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'question_text': 'changed',
        'pub_date': '2020-10-15T00:00:00Z',
        'choices': [
            {'choice_text': 'choice 1 changed', 'id': 1, 'votes': 10},
            {'choice_text': 'new choice', 'id': 2, 'votes': 0}
        ]
    }


@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_updated_for_invalid_data():
    """Tests getting a question."""
    question = Question.objects.create(
        question_text="First question.",
        pub_date=datetime.now()
    )

    Choice.objects.create(question=question, choice_text="Choice 1", votes=10)

    client = Client()

    valid_data = {
            "question_text": "changed",
            "pub_date": "2020-10-15",
            "choices": [
                {
                    "id": 10,
                    "choice_text": "choice 1 changed"
                },
                {
                    "choice_text": "new choice"
                }
            ]
        }

    response = client.put('/polls/question/1', json.dumps(valid_data))

    assert response.status_code == 400
    assert response.json() == {"message": "Choice matching query does not exist.", "status": "error"}
