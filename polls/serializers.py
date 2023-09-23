"""Covers all the serializers for models."""
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.exceptions import ValidationError

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """The question serializer."""
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField("date published")

    class Meta:
        model = Question
        fields = '__all__'

    @classmethod
    def create(cls, data: dict):
        """Creates a model in the database."""
        serializer = cls(data=data)

        if serializer.is_valid():
            question = Question.objects.create(**serializer.validated_data)
        else:
            raise ValidationError("data was not validated.")

        return question
