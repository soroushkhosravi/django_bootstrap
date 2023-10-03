"""Views related to the polls application."""
from django.http import HttpResponse, JsonResponse
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from application_services import get_question_service
from repositories import get_question_repository


def index(request):
    get_question_service().add_question(question_text="A question from app service.")
    try:
        k = JSONParser().parse(request)
        return JsonResponse(k)
    except (ParseError, TypeError):
        return JsonResponse( {"message": "Wrong request data structure."}, status=400)
    return JsonResponse({"message": "successful."}, status=400)

def get_question(request, question_id):
    """return poll with id."""
    question =get_question_repository().get_question(question_id=question_id)
    if question:
        return JsonResponse({"message": "successful."})

    return HttpResponse("Question not found..")

