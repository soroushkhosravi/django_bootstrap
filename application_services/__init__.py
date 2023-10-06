"""The factory to create application services."""
from django.core.cache import caches

from repositories import get_question_repository
from serializers.question import QuestionSerializer
from .question import QuestionService


def get_question_service(cache=None):
    return QuestionService(
        repo=get_question_repository(),
        cache=cache or caches["default"],
        data_serializer=QuestionSerializer
    )