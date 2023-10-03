"""The question application service to do actions on questions."""
from repositories.question import QuestionRepo
from django.utils import timezone
from serializers.question import QuestionSerializer

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

    def get_question(self, question_id: int):
        """Returns a question data by it's ID."""
        question = self._repo.get_question(question_id=question_id)

        if not question:
            raise Exception("Question not found.")

        return QuestionSerializer(question).data


