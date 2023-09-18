import pytest

from django.contrib.auth.models import User
from polls.models import Question
from polls.repos import get_question_service, get_question_repo


@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
  assert User.objects.count() == 1

@pytest.mark.django_db
def test_question_create():
  get_question_repo().add_question()
  assert Question.objects.count() == 1
  assert User.objects.count() == 0