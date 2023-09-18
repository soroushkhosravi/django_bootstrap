"""The definition of the question repository to find models."""
from polls.models import Question

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