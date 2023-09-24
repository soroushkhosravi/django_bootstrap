"""Tests related to the choice serializer."""
import pytest
from polls.serializers import ChoiceSerializer

@pytest.mark.parametrize(
    "data, is_valid, validated_data",
    [
        (
            {
                "choice_text": "A choice"
            },
            True,
            {
                "choice_text": "A choice"
            }
        ),
        (
            {
                "votes": 10,
            },
            False,
            {}
        ),
        (
            {
                "choice_text": "A choice",
                "votes": 10
            },
            True,
            {
                "choice_text": "A choice",
                "votes": 10
            }
        )
    ]
)
@pytest.mark.django_db(reset_sequences=True)
def test_choice_serializer(data, is_valid, validated_data):
    """Tests validating data."""
    serializer = ChoiceSerializer(data=data)
    assert ChoiceSerializer(data=data).is_valid() is is_valid