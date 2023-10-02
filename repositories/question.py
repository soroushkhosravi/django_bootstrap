"""The definition of the question repository to find models."""
from cursor_pagination import CursorPaginator
from typing import Optional

from polls.models import Question
from .entity_list import EntityList


class QuestionRepo():
    """Repo for finding question models."""
    def __init__(self, model):
        self._model = model

    def get_question(self, question_id):
        """Finds a question by it's id."""
        try:
            return self._model.objects.get(pk=question_id)
        except self._model.DoesNotExist:
            return None

    def all(self, page_size: int, last: str = None):
        """Getting all the questions."""
        questions = self._model.objects.all()
        paginator = CursorPaginator(questions, ordering=('-id',))
        page = paginator.page(first=page_size, after=last)

        return EntityList(
            iterable=page,
            last_cursor=paginator.cursor(page[-1]),
        )

