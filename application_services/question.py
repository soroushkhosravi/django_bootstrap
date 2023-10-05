"""The question application service to do actions on questions."""
from repositories.question import QuestionRepo
from django.utils import timezone
from exceptions import ServiceException, SerializerException
from polls.models import Question


class QuestionService:
    def __init__(
        self,
        repo: QuestionRepo,
        cache,
        data_serializer
    ):
        self._repo = repo
        self._cache = cache
        self._data_serializer = data_serializer

    def add_question(self, question_text: str) -> Question:
        """Adds a question to the database."""
        question = self._repo._model(question_text=question_text, pub_date=timezone.now())
        question.save()
        return question

    def get_question(self, question_id: int) -> dict:
        """Returns a question data by it's ID."""
        question = self._repo.get_question(question_id=question_id)

        if not question:
            raise ServiceException("Question not found.")

        return self._data_serializer(question).data

    def update_question(self, question_id, question_data) -> dict:
        """Updates a question by it's ID."""
        question = self._repo.get_question(question_id=question_id)

        if not question:
            raise ServiceException("Question not found.")

        serializer = self._data_serializer(question, data=question_data)

        if serializer.is_valid():
            serializer.update(instance=question, validate_data=serializer.validated_data)
        else:
            raise SerializerException(message="Data could not be serialized.", errors=serializer.errors)

        return serializer.data

    def delete_question(self, question_id: int) -> None:
        """Deletes a question."""
        question = self._repo.get_question(question_id=question_id)

        if not question:
            raise ServiceException("Question not found.")

        question.delete()
