"""Tests related to the question model."""
import pytest

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

