"""Covers all the serializers for models."""
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.exceptions import ValidationError
from django.db import transaction

from .models import Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    """The choice serializer."""
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']


class QuestionSerializer(serializers.ModelSerializer):
    """The question serializer."""
    question_choices = ChoiceSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Question
        fields = '__all__'

    def create(self, validated_data: dict):
        """Creates a model in the database."""
        try:
            question_choices = validated_data.pop('question_choices')
        except KeyError:
            question_choices = []
        question = Question.objects.create(**validated_data)

        for choice in question_choices:
            Choice.objects.create(question=question, **choice)

        return question

    def update(self, instance, validate_data: dict):
        """Updates an instance through passed data."""
        try:
            with transaction.atomic():
                instance.question_text = validate_data.get("question_text", instance.question_text)
                instance.pub_date = validate_data.get("pub_date", instance.pub_date)
                instance.save()
                if choices := validate_data.get("question_choices"):
                    for choice in choices:
                        if choice.get("id"):
                            question_choice = instance.choices.get(pk=choice["id"])
                            question_choice.choice_text = choice.get(
                                "choice_text", question_choice.choice_text
                            )
                        else:
                            Choice.objects.create(**choice, question=instance)
        except Exception:
            pass

        return instance
