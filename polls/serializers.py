"""Covers all the serializers for models."""
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail, ValidationError

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """The question serializer."""
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField("date published")

    class Meta:
        model = Question
        # fields = ("id", "question_text", "pub_date")
        fields = '__all__'
