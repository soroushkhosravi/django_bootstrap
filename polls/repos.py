from polls.models import Choice, Question
from django.utils import timezone

class QuestionRepo:
    """Repo for fiding questions."""
    _model = Question

    def add_question(self):
        question = self._model(question_text="What's new?", pub_date=timezone.now())
        question.save()

    def get_question(self, question_id):
        """"""
        try:
            return self._model.objects.get(pk=question_id)
        except self._model.DoesNotExist:
            return None

def get_question_repo():
    """Returns a repository."""
    return QuestionRepo()

class QuestionService():
    def __init__(self, repo):
        self._repo = repo

    def add_question(self):
        self._repo.add_question()


def get_question_service():
    return QuestionService(repo=get_question_repo())