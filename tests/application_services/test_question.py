"""Tests related to the question application service."""
from application_services import get_question_service
import pytest
from polls.models import Question
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




