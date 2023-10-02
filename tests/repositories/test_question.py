"""Tests related to the question repository."""
from repositories import get_question_repository
import pytest
from polls.models import Question
from datetime import datetime
from repositories.question import EntityList


@pytest.mark.django_db(reset_sequences=True)
def test_get_all():
    """Tests related getting all questions."""
    Question.add_with_choices(
        text="First question.",
        pub_date=datetime.now(),
        choices=["This is choice one.", "This is choice two."]
    )

    Question.add_with_choices(
        text="Second question.",
        pub_date=datetime.now(),
        choices=["This is choice one.", "This is choice two."]
    )

    Question.add_with_choices(
        text="Third question.",
        pub_date=datetime.now(),
        choices=["This is choice one.", "This is choice two."]
    )

    page = get_question_repository().all(page_size=2)

    assert isinstance(page, EntityList)
    assert len(page) == 2
    assert page.has_next == True
    assert page.has_previous == False
    assert page.last_cursor == "Mg=="

    assert page[0].id == 3
    assert page[1].id == 2

    page2 = get_question_repository().all(page_size=2, last=page.last_cursor)

    assert isinstance(page2, EntityList)
    assert len(page2) == 1
    assert page2.has_next == False
    assert page2.has_previous == True
    assert page2.last_cursor == "MQ=="

    assert page2[0].id == 1

    page_with_all_models = get_question_repository().all(page_size=5, last=None)

    assert len(page_with_all_models) == 3
    assert page_with_all_models.has_next == False
    assert page_with_all_models.has_previous == False
    assert page_with_all_models.last_cursor == "MQ=="

    assert page_with_all_models[0].id == 3
    assert page_with_all_models[1].id == 2
    assert page_with_all_models[2].id == 1