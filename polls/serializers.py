"""Covers all the serializers for models."""
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.exceptions import ValidationError

from .models import Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    """The choice serializer."""
    class Meta:
        model = Choice
        fields = ['choice_text', 'votes']


class QuestionSerializer(serializers.ModelSerializer):
    """The question serializer."""
    question_choices = ChoiceSerializer(many=True, required=False)

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
