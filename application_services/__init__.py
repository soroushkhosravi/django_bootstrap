"""The factory to create application services."""
from .question import QuestionService
from repositories import get_question_repository

def get_question_service():
    return QuestionService(repo=get_question_repository())