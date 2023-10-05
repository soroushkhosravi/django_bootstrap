"""Tests related to the question application service."""
from collections import OrderedDict
from datetime import datetime

import pytest
from freezegun import freeze_time

from application_services import get_question_service
from exceptions import ServiceException
from polls.models import Choice, Question


@pytest.fixture
def service():
    """A fixture for the tests."""
    return get_question_service()


@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_get_question_data_returns_expected_data(service):
    """Tests we can get the question's data."""
    question = Question.objects.create(
        question_text="First question",
        pub_date=datetime.now()
    )
    Choice.objects.create(
        choice_text="Choice 1",
        question=question
    )

    Choice.objects.create(
        choice_text="Choice 2",
        question=question
    )

    data = service.get_question(question_id=1)

    assert data == {
        'id': 1,
        'pub_date': '2020-10-10T00:00:00Z',
        'question_text': 'First question',
        'choices': [
            OrderedDict([('id', 1), ('choice_text', 'Choice 1'), ('votes', 0)]),
            OrderedDict([('id', 2), ('choice_text', 'Choice 2'), ('votes', 0)])
        ]
    }


@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_update_question_updates_question_as_expected(service):
    """Tests we can get the question's data."""
    Question.objects.create(
        question_text="First question",
        pub_date=datetime.now()
    )

    data = service.update_question(
        question_id=1,
        question_data={
            "question_text": "changed",
            "pub_date": "2020-10-15",
        }
    )

    assert data == {'id': 1, 'pub_date': '2020-10-15T00:00:00Z', 'question_text': 'changed', 'choices': []}


@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_update_question_raises_exception_if_data_not_valid(service):
    """Tests we can get the question's data."""
    Question.objects.create(
        question_text="First question",
        pub_date=datetime.now()
    )

    with pytest.raises(ServiceException) as error:
        service.update_question(
            question_id=1,
            question_data={"invalid_key": "invalid_value"}
        )

    assert str(error.value) == (
        "{'question_text': [ErrorDetail(string='This field is required.', code='required')], "
        "'pub_date': [ErrorDetail(string='This field is required.', code='required')]}"
    )


@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_delete_deletes_specific_question(service):
    """Tests we can get the question's data."""
    question = Question.objects.create(
        question_text="First question",
        pub_date=datetime.now()
    )
    Choice.objects.create(choice_text="choice", question=question)
    questions = Question.objects.all()

    assert len(questions) == 1

    service.delete_question(question_id=1)

    questions = Question.objects.all()
    assert len(questions) == 0
