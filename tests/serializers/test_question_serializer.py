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
                        ("question_choices", [{"choice_text": "abc"}]),
                        ("question_text", "abc"),
                        ("pub_date", datetime(year=2000, month=10, day=5, tzinfo=ZoneInfo(key="UTC"))),
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
        ),
        (
                {
                    "question_text": "abc",
                    "pub_date": timezone.datetime(year=2000, month=10, day=5)
                },
                True,
                OrderedDict(
                    [
                        ("question_text", "abc"),
                        ("pub_date", datetime(year=2000, month=10, day=5, tzinfo=ZoneInfo(key="UTC"))),
                    ]
                )
        ),
        (
                {
                    "question_text": "abc",
                    "pub_date": timezone.datetime(year=2000, month=10, day=5),
                    "question_choices": [
                        {
                            "votes": 5
                        }
                    ]
                },
                False,
                {}
        ),
    ]
)
def test_serializer_validates_data_as_expected(data, is_valid, validated_data):
    """Tests we can validate data passed to serializer."""
    serializer = QuestionSerializer(data=data)
    assert serializer.is_valid() is is_valid
    assert serializer.validated_data == validated_data


@pytest.mark.django_db(reset_sequences=True)
def test_create_adds_question_to_the_database_with_choices():
    """Tests we can add models to database with serializer."""
    all_questions = get_question_repository()._model.objects.all()

    assert len(all_questions) == 0

    valid_data = {
        "question_text": "abc",
        "pub_date": datetime(year=2000, month=10, day=5),
        "question_choices": [{"choice_text": "abc"}]
    }

    serializer = QuestionSerializer(data=valid_data)
    serializer.is_valid()
    serializer.save()

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
def test_create_adds_question_itself_if_choices_not_provided():
    """Tests we can add models to database with serializer."""
    all_questions = get_question_repository()._model.objects.all()

    assert len(all_questions) == 0

    valid_data = {
        "question_text": "abc",
        "pub_date": datetime(year=2000, month=10, day=5)
    }

    serializer = QuestionSerializer(data=valid_data)
    serializer.is_valid()
    serializer.save()

    all_questions = get_question_repository()._model.objects.all()
    assert len(all_questions) == 1

    added_question = all_questions[0]

    assert added_question.id == 1
    assert added_question.question_text == valid_data["question_text"]
    assert added_question.pub_date == datetime(2000, 10, 5, 0, 0, tzinfo=ZoneInfo(key="UTC"))
    assert len(added_question.choices.all()) == 0


@pytest.mark.django_db(reset_sequences=True)
def test_serializer_raises_exception_if_saved_with_invalid_data():
    """Tests we can add models to database with serializer."""
    all_questions = get_question_repository()._model.objects.all()

    assert len(all_questions) == 0

    invalid_data = {"question_text": "abc"}

    serializer = QuestionSerializer(data=invalid_data)
    serializer.is_valid()

    assert serializer.validated_data == {}
    assert serializer.errors is not None

    with pytest.raises(AssertionError) as error:
        serializer.save()

    assert str(error.value) == (
        "You cannot call `.save()` on a serializer with invalid data."
    )


@pytest.mark.django_db(reset_sequences=True)
def test_serializer_can_update_instance():
    """Tests we can add models to database with serializer."""
    question = Question.objects.create(
        question_text="question",
        pub_date=datetime.now()
    )
    choice = Choice.objects.create(
        choice_text="abc",
        question=question
    )
    assert question.id == 1

    valid_data = {
        "question_text": "changed",
        "pub_date": "2023-09-24T16:42:23.771150",
        "question_choices": [
            {
                "choice_text": "choice 1"
            }
        ]
    }

    serializer =QuestionSerializer(question, data=valid_data)

    assert serializer.is_valid() is True
    serializer.save()

    assert question.id == 1
    assert question.question_text == "changed"
    assert question.pub_date == datetime(
        2023, 9, 24, 16, 42, 23, 771150,  tzinfo=ZoneInfo(key="UTC")
    )

    choices = question.choices.all()
    assert len(choices) == 2

    assert choices[0].id == 1
    assert choices[1].id == 2
    assert choices[1].choice_text == "choice 1"


@pytest.mark.django_db(reset_sequences=True)
def test_updating_existing_choice_through_question():
    """."""
    question = Question.objects.create(
        question_text="question",
        pub_date=datetime.now()
    )
    Choice.objects.create(
        choice_text="abc",
        question=question
    )
    assert question.id == 1

    valid_data = {
        "question_text": "changed",
        "pub_date": "2023-09-24T16:42:23.771150",
        "question_choices": [
            {
                "choice_text": "choice 1",
                "id": 1
            }
        ]
    }

    serializer =QuestionSerializer(question, data=valid_data)

    assert serializer.is_valid() is True
    serializer.save()

    assert question.id == 1
    assert question.question_text == "changed"
    assert question.pub_date == datetime(
        2023, 9, 24, 16, 42, 23, 771150,  tzinfo=ZoneInfo(key="UTC")
    )

    choices = question.choices.all()
    assert len(choices) == 1

    assert choices[0].id == 1
    assert choices[0].choice_text == "choice 1"
