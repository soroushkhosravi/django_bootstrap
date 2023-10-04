"""Tests related to the Question application service."""
import fakeredis
import pytest

from application_services import get_question_service, QuestionService
from polls.models import Question


@pytest.fixture()
def service() -> QuestionService:
    """Fixture for the tests."""
    return get_question_service(cache=fakeredis.FakeStrictRedis())


@pytest.mark.django_db(reset_sequences=True)
def test_service_initiation(service):
    """Tests the creation of the service."""
    assert isinstance(service, QuestionService)


@pytest.mark.django_db(reset_sequences=True)
def test_service_can_add_model_and_sets_id_in_cache(service):
    """Tests adding the question and setting the ID in cache."""
    assert service._cache.get(1) is None
    assert len(Question.objects.all()) == 0

    service.add_question(question_text="This is a question.")
    assert len(Question.objects.all()) == 1
