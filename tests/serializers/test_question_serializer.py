"""Tests related to the question serializer."""
import pytest
from collections import OrderedDict
from datetime import datetime
from django.utils import timezone
from zoneinfo import ZoneInfo

from polls.serializers import QuestionSerializer


@pytest.mark.parametrize(
    "data, is_valid, validated_data",
    [
        (
            {"question_text": "abc", "pub_date": timezone.datetime(year=2000, month=10, day=5)},
            True,
            OrderedDict(
                [
                    ("question_text", "abc"),
                    ("pub_date", datetime(year=2000, month=10, day=5, tzinfo=ZoneInfo(key="UTC")))
                ]
            )
        ),
        (
            {"pub_date": timezone.now()},
            False,
            {}
        ),
        (
            {"question_text": "abc", "pub_date": 100},
            False,
            {}
        )
    ]
)
def test_serializer_validates_data_as_expected(data, is_valid, validated_data):
    """Tests we can validate data passed to serializer."""
    serializer = QuestionSerializer(data=data)
    assert serializer.is_valid() is is_valid
    assert serializer.validated_data == validated_data
