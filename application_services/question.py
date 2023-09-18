"""The question application service to do actions on questions."""
from repositories.question import QuestionRepo
from django.utils import timezone

class QuestionService:
    def __init__(self, repo: QuestionRepo):
        self._repo = repo

    def add_question(self, question_text: str):
        """Adds a question to the database."""
        question = self._repo._model(question_text=question_text, pub_date=timezone.now())
        question.save()
        return question

