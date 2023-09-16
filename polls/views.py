from django.http import HttpResponse
from polls.repos import get_question_service

def index(request):
    get_question_service().add_question()
    return HttpResponse("Hello, question saved successfully.")
