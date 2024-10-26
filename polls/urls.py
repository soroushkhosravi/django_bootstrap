from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("question/<int:question_id>", views.question, name="question"),
    path("first", views.show_template, name="first"),
    path("token", views.get_token_for, name="token")
]