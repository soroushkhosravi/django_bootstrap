"""Views related to the polls application."""
from django.http import HttpResponse, JsonResponse

from application_services import get_question_service
from repositories import get_question_repository


def index(request):
    get_question_service().add_question(question_text="A question from app service.")
    return JsonResponse({"message": "successful."}, status=200)


def get_question(request, question_id):
    """return poll with id."""
    question = get_question_repository().get_question(question_id=question_id)
    if question:
        return JsonResponse({"message": "successful."})

    return HttpResponse("Question not found.", status=400)

