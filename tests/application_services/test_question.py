"""Tests related to the question application service."""
from collections import OrderedDict
from datetime import datetime

import pytest
from freezegun import freeze_time

from application_services import get_question_service, QuestionService
from exceptions import ServiceException, SerializerException
from polls.models import Choice, Question


@pytest.fixture
def service() -> QuestionService:
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
    """Tests we can update the questions' data."""
    question = Question.objects.create(
        question_text="First question",
        pub_date=datetime.now()
    )

    assert question.id == 1
    assert question.question_text == "First question"
    assert question.pub_date == datetime.now()

    data = service.update_question(
        question_id=1,
        question_data={
            "question_text": "changed",
            "pub_date": "2020-10-15",
            "choices": []
        }
    )

    question = Question.objects.filter(pk=1)[0]
    assert question.question_text == "changed"

    assert data == {'id': 1, 'pub_date': '2020-10-15T00:00:00Z', 'question_text': 'changed', 'choices': []}


@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_update_question_updates_question_choices_as_expected(service):
    """Tests we can update the questions' data."""
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

    assert question.id == 1
    assert question.question_text == "First question"
    assert question.pub_date == datetime.now()

    assert len(question.choices.all()) == 2

    data = service.update_question(
        question_id=1,
        question_data={
            "question_text": "changed",
            "pub_date": "2020-10-15",
            "choices": [
                {
                    "id": 1,
                    "choice_text": "choice 1 changed"
                }
            ]
        }
    )

    question = Question.objects.filter(pk=1)[0]
    assert question.question_text == "changed"

    assert question.choices.all()[0].id == 1
    assert question.choices.all()[0].choice_text == "choice 1 changed"

    assert question.choices.all()[1].id == 2
    assert question.choices.all()[1].choice_text == "Choice 2"

    assert data == {
        'id': 1,
        'question_text': 'changed',
        'pub_date': '2020-10-15T00:00:00Z',
        'choices': [
            OrderedDict([('id', 1), ('choice_text', 'choice 1 changed'), ('votes', 0)]),
            OrderedDict([('id', 2), ('choice_text', 'Choice 2'), ('votes', 0)])
        ]
    }


@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_update_question_raises_expected_error_and_is_transactional(service):
    """Tests if error happens, nothing is updated."""
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

    assert question.id == 1
    assert question.question_text == "First question"
    assert question.pub_date == datetime.now()

    assert len(question.choices.all()) == 2

    with pytest.raises(Choice.DoesNotExist) as error:
        data = service.update_question(
            question_id=1,
            question_data={
                "question_text": "changed",
                "pub_date": "2020-10-15",
                "choices": [
                    {
                        "id": 10,
                        "choice_text": "choice 1 changed"
                    }
                ]
            }
        )

    assert str(error.value) == "Choice matching query does not exist."

    question = Question.objects.filter(pk=1)[0]
    assert question.question_text == "First question"

    assert question.choices.all()[0].id == 1
    assert question.choices.all()[0].choice_text == "Choice 1"

    assert question.choices.all()[1].id == 2
    assert question.choices.all()[1].choice_text == "Choice 2"


@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_update_question_raises_exception_if_data_not_valid(service):
    """Tests we can get the question's data."""
    Question.objects.create(
        question_text="First question",
        pub_date=datetime.now()
    )

    with pytest.raises(SerializerException) as error:
        service.update_question(
            question_id=1,
            question_data={"invalid_key": "invalid_value"}
        )

    assert str(error.value) == (
        "Data could not be serialized."
        "{'question_text': [ErrorDetail(string='This field is required.', code='required')], "
        "'pub_date': [ErrorDetail(string='This field is required.', code='required')]}"
    )


@freeze_time("2020-10-10")
@pytest.mark.django_db(reset_sequences=True)
def test_update_question_adds_choice_if_choice_id_not_passed(service):
    """Tests we can get the question's data."""
    question = Question.objects.create(
        question_text="First question",
        pub_date=datetime.now()
    )

    Choice.objects.create(
        choice_text="Choice 1",
        question=question
    )

    assert question.id == 1
    assert question.question_text == "First question"
    assert question.pub_date == datetime.now()

    assert len(question.choices.all()) == 1

    data = service.update_question(
        question_id=1,
        question_data={
            "question_text": "changed",
            "pub_date": "2020-10-15",
            "choices": [
                {
                    "id": 1,
                    "choice_text": "choice 1 changed"
                },
                {
                    "choice_text": "choice 2"
                }
            ]
        }
    )

    question = Question.objects.filter(pk=1)[0]
    assert question.question_text == "changed"

    assert question.choices.all()[0].id == 1
    assert question.choices.all()[0].choice_text == "choice 1 changed"

    assert question.choices.all()[1].id == 2
    assert question.choices.all()[1].choice_text == "choice 2"

    assert data == {
        'id': 1,
        'question_text': 'changed',
        'pub_date': '2020-10-15T00:00:00Z',
        'choices': [
            OrderedDict([('id', 1), ('choice_text', 'choice 1 changed'), ('votes', 0)]),
            OrderedDict([('id', 2), ('choice_text', 'choice 2'), ('votes', 0)])
        ]
    }


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
