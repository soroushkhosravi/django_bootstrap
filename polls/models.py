from django.db import models
from datetime import datetime
from django.db import transaction


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def choices_with_specific_votes(self, number_of_votes: int):
        """Returns all the chices with 5 votes."""
        return self.choices.filter(votes=number_of_votes)

    @classmethod
    def add_with_choices(
            cls,
            text: str,
            pub_date: datetime,
            choices: list
    ):
        """Adds a question with choices."""
        with transaction.atomic():
            question = cls(question_text=text, pub_date=pub_date)
            question.save()

            for choice_text in choices:
                choice = Choice(
                    question=question,
                    choice_text=choice_text
                )
                choice.save()



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
