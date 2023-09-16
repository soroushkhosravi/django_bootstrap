from django.http import HttpResponse
from polls.repos import get_question_service, get_question_repo
from polls.models import Question

def index(request):
    get_question_service().add_question()
    return HttpResponse("Hello, question saved successfully.")

def get_question(request, question_id):
    """return poll with id."""
    question =get_question_repo().get_question(question_id=question_id)
    if question:
        return HttpResponse(question.id)

    return HttpResponse("Question not found..")

