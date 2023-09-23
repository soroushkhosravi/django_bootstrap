"""Tests related to the question serializer."""
import pytest
from collections import OrderedDict
from datetime import datetime
from django.utils import timezone
from zoneinfo import ZoneInfo

from polls.serializers import QuestionSerializer, ChoiceSerializer
from repositories import get_question_repository
from polls.models import Question, Choice


@pytest.mark.parametrize(
    "data, is_valid, validated_data",
    [
        (
            {
                "question_text": "abc",
                "pub_date": timezone.datetime(year=2000, month=10, day=5),
                "question_choices": [
                    {
                        "choice_text": "abc"
                    }
                ]
            },
            True,
            OrderedDict(
                [
                    ("question_text", "abc"),
                    ("pub_date", datetime(year=2000, month=10, day=5, tzinfo=ZoneInfo(key="UTC"))),
                    ("question_choices", [{"choice_text": "abc"}]),
                ]
            )
        ),
        (
            {"pub_date": timezone.now()},
            False,
            {}
        ),
        (
            {"question_text": "abc", "pub_date": 100},
            False,
            {}
        )
    ]
)
def test_serializer_validates_data_as_expected(data, is_valid, validated_data):
    """Tests we can validate data passed to serializer."""
    serializer = QuestionSerializer(data=data)
    assert serializer.is_valid() is is_valid
    assert serializer.validated_data == validated_data


@pytest.mark.django_db(reset_sequences=True)
def test_create_adds_model_to_the_database():
    """Tests we can add models to database with serializer."""
    all_questions = get_question_repository()._model.objects.all()

    assert len(all_questions) == 0

    valid_data = {
        "question_text": "abc",
        "pub_date": datetime(year=2000, month=10, day=5),
        "question_choices": [{"choice_text": "abc"}]
    }

    QuestionSerializer.create(data=valid_data)

    all_questions = get_question_repository()._model.objects.all()

    assert len(all_questions) == 1

    added_question = all_questions[0]

    assert added_question.id == 1
    assert added_question.question_text == valid_data["question_text"]
    assert added_question.pub_date == datetime(2000, 10, 5, 0, 0, tzinfo=ZoneInfo(key="UTC"))
    assert len(added_question.choices.all()) == 1

    choice = added_question.choices.all()[0]

    assert isinstance(choice, Choice)
    assert choice.id == 1
    assert choice.question_id == 1
    assert choice.votes == 0
    assert choice.choice_text == "abc"


@pytest.mark.django_db(reset_sequences=True)
def test_create_does_not_add_model_to_the_database_with_invalid_date():
    """Tests we can add models to database with serializer."""
    all_questions = get_question_repository()._model.objects.all()

    assert len(all_questions) == 0

    invalid_data = {"question_text": "abc"}
    with pytest.raises(Exception) as error:
        QuestionSerializer.create(data=invalid_data)

    assert str(error.value) == "[ErrorDetail(string='data was not validated.', code='invalid')]"

    all_questions = get_question_repository()._model.objects.all()

    assert len(all_questions) == 0

@pytest.mark.django_db(reset_sequences=True)
def test_choice_serializer():
    """Tests validating data."""
    data = {
        "choice_text": "This is a text",
        "votes": 10
    }

    assert ChoiceSerializer(data=data).is_valid() == True