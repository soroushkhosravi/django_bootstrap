import pytest

from django.contrib.auth.models import User
from polls.models import Question

from repositories import get_question_repository
from django.utils import timezone
from application_services import get_question_service


@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
  assert User.objects.count() == 1

  users = User.objects.all()

  assert len(users) == 1

  assert users[0].id == 1
  assert users[0].email == 'lennon@thebeatles.com'
  assert isinstance(users[0], User)
  assert users[0].username == 'john'
  assert users[0].first_name == ''
  assert users[0].last_name == ''

@pytest.mark.django_db(reset_sequences=True)
def test_question_create():
  get_question_service().add_question(question_text="abc")
  assert Question.objects.count() == 1
  assert User.objects.count() == 0

@pytest.mark.django_db(reset_sequences=True)
def test_question_repository():
  """Tests the question repository."""
  question = get_question_repository().get_question(question_id=1)

  assert question is None
  assert Question.objects.count() == 0

  question = get_question_repository()._model(question_text="What's new?", pub_date=timezone.now())
  question.save()

  question = Question.objects.get(pk=1)

  assert question.id == 1

@pytest.mark.django_db(reset_sequences=True)
def test_question_service():
  """Tests the question repository."""
  question = get_question_service().add_question(question_text="This is a question.")

  assert question.id == 1
  assert question.question_text == "This is a question."



