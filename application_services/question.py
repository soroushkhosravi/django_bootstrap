"""The question application service to do actions on questions."""
from repositories.question import QuestionRepo
from django.utils import timezone

class QuestionService:
    def __init__(
            self,
            repo: QuestionRepo,
            cache
    ):
        self._repo = repo
        self._cache = cache

    def add_question(self, question_text: str):
        """Adds a question to the database."""
        question = self._repo._model(question_text=question_text, pub_date=timezone.now())
        question.save()
        self._cache.set(str(question.id), question.question_text)
        return question

