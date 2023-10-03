"""The factory to create application services."""
from .question import QuestionService
from repositories import get_question_repository
from django.core.cache import caches
from serializers.question import QuestionSerializer

def get_question_service(cache=None):
    return QuestionService(
        repo=get_question_repository(),
        cache= cache or caches["default"],
        data_serializer=QuestionSerializer
    )