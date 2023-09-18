from django.http import HttpResponse
from application_services import get_question_service
from repositories import get_question_repository
from polls.models import Question

def index(request):
    get_question_service().add_question(question_text="A question from app service.")
    return HttpResponse("Hello, question saved successfully.")

def get_question(request, question_id):
    """return poll with id."""
    question =get_question_repository().get_question(question_id=question_id)
    if question:
        return HttpResponse(question.id)

    return HttpResponse("Question not found..")

