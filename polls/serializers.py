"""Covers all the serializers for models."""
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.exceptions import ValidationError

from .models import Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    """The choice serializer."""
    id = serializers.IntegerField(read_only=True)
    choice_text = serializers.CharField(max_length=200)
    votes = serializers.IntegerField()

    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """The question serializer."""
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField("date published")
    question_choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'

    @classmethod
    def create(cls, data: dict):
        """Creates a model in the database."""
        serializer = cls(data=data)
        if serializer.is_valid():
            question_choices = serializer.validated_data.pop('question_choices')
            question = Question.objects.create(**serializer.validated_data)

            for choice in question_choices:
                Choice.objects.create(question=question, **choice)
        else:
            raise ValidationError("data was not validated.")

        return question
