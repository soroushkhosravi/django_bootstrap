"""Tests related to the question application service."""
from application_services import get_question_service
import pytest
from polls.models import Question, Choice
from datetime import datetime
from freezegun import freeze_time

@pytest.fixture
def service():
    """A fixture for the tests."""
    return get_question_service()

@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_get_question_data_returns_expected_data(service):
    """Tests we can get the question's data."""
    Question.objects.create(
        question_text="First question",
        pub_date=datetime.now()
    )

    data = service.get_question(question_id=1)

    assert data == {'id': 1, 'pub_date': '2020-10-10T00:00:00Z', 'question_text': 'First question'}

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
            "pub_date": "2020-10-15"
        }
    )

    assert data == {'id': 1, 'pub_date': '2020-10-15T00:00:00Z', 'question_text': 'changed'}


@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_update_question_raises_exception_if_data_not_valid(service):
    """Tests we can get the question's data."""
    Question.objects.create(
        question_text="First question",
        pub_date=datetime.now()
    )

    with pytest.raises(Exception) as error:
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