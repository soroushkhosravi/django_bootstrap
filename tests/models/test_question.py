"""Tests related to the question model."""
import pytest
from django.db import transaction

from polls.models import Question, Choice
from datetime import datetime

@pytest.mark.django_db(reset_sequences=True)
def test_question_service():
    """Tests the question repository."""
    question = Question(
      question_text="This is a question.",
      pub_date=datetime.now()
    )

    assert isinstance(question, Question)
    question.save()

    choice = Choice(
      choice_text="This is choice text.",
      votes=10,
      question=question
    )
    choice.save()
    assert len(question.choices.all()) == 1

    assert question.id == 1
    assert question.question_text == "This is a question."

    choice = question.choices.all()[0]

    assert isinstance(choice, Choice)
    assert choice.id == 1
    assert choice.question_id == question.id == 1

    existing_choice = question.choices.filter(choice_text="This is choice text.")[0]

    assert existing_choice.id == 1

    not_existing_choice = question.choices.filter(choice_text="This is not choice text.")

    assert len(not_existing_choice) ==0


@pytest.mark.django_db(reset_sequences=True)
def test_choices_with_five_votes():
    """Tests the question repository."""
    question = Question(
      question_text="This is a question.",
      pub_date=datetime.now()
    )

    assert isinstance(question, Question)
    question.save()

    choice = Choice(
      choice_text="This is choice text.",
      votes=10,
      question=question
    )
    choice.save()

    choice = Choice(
      choice_text="This is choice text.",
      votes=5,
      question=question
    )
    choice.save()
    assert len(question.choices.all()) == 2

    assert question.id == 1
    assert question.question_text == "This is a question."

    choices_with_five_votes = (
        question.choices_with_specific_votes(number_of_votes=5)
    )

    assert len(choices_with_five_votes) == 1

    choice_with_five_vote = choices_with_five_votes[0]

    assert choice_with_five_vote.id == 2
    assert choice_with_five_vote.votes == 5

@pytest.mark.django_db(reset_sequences=True)
def test_add_with_choices():
    """Tests the add_with_choices function."""
    Question.add_with_choices(
        text="This is a question.",
        pub_date=datetime.now(),
        choices=["This is choice one.", "This is choice two."]
    )

    questions = Question.objects.all()

    assert len(questions) == 1
    assert questions[0].id == 1

    assert len(questions[0].choices.all()) == 2

    assert questions[0].choices.all()[0].id == 1
    assert questions[0].choices.all()[0].choice_text == (
        "This is choice one."
    )
    assert questions[0].choices.all()[1].choice_text == (
        "This is choice two."
    )


