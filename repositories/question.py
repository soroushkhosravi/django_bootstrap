"""The definition of the question repository to find question models."""
from typing import Optional

from cursor_pagination import CursorPaginator

from polls.models import Question
from .entity_list import EntityList


class QuestionRepo:
    """Repo for finding question models."""
    def __init__(self, model):
        self._model = model

    def get_question(self, question_id: int) -> Optional[Question]:
        """Returns a question by it's ID.

        Args:
            question_id: The ID of the question.

        Returns:
            A question if exists by the defined ID.
        """
        try:
            return self._model.objects.get(pk=question_id)
        except self._model.DoesNotExist:
            return None

    def all(self, page_size: int, last: str = None) -> EntityList:
        """Getting all the questions based on cursor based pagination.

        Args:
            page_size: The size of the page.
            last: The last cursor string which shows end of previous page.

        Returns:
            An EntityList including the questions and the last cursor of the page.
        """
        questions = self._model.objects.all()
        paginator = CursorPaginator(questions, ordering=('-id',))
        page = paginator.page(first=page_size, after=last)

        return EntityList(
            iterable=page,
            last_cursor=paginator.cursor(page[-1]),
        )

