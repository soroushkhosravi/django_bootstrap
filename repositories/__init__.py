"""The factories to get the repositories."""
from .question import QuestionRepo
from polls.models import Question

def get_question_repository():
    """Returns a question repository."""
    return QuestionRepo(model=Question)