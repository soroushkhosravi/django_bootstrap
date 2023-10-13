"""Views related to the polls application."""
from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from application_services import get_question_service
from exceptions import ServiceException, SerializerException
from rest_framework.parsers import JSONParser
from src.crema.domain.books import create_book, create_cook


def index(request):
    create_book(book_title="The first book")
    create_cook(cook_name="soroush")
    return JsonResponse({"message": "successful."}, status=200)


@csrf_exempt
def question(request, question_id):
    """handles all actions related to question."""
    question_service = get_question_service()
    if request.method == 'GET':
        try:
            return JsonResponse(question_service.get_question(question_id=question_id))
        except ServiceException as error:
            return JsonResponse(data={"message": str(error), "status": "error"}, status=400)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        try:
            data = question_service.update_question(question_id=question_id, question_data=data)
            return JsonResponse(data=data)
        except (ServiceException, SerializerException) as error:
            return JsonResponse(data={"message": str(error), "status": "error"}, status=400)

    elif request.method == "DELETE":
        try:
            question_service.delete_question(question_id=question_id)
        except ServiceException as error:
            return JsonResponse(data={"message": str(error), "status": "error"}, status=400)
        return JsonResponse({"message": f"question {question_id} deleted.", "status": "success"})


