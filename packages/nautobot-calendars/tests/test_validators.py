import pytest
from django.core.exceptions import ValidationError
from nautobot_calendars.validators import JSONSchemaValidator


def test_jsonschema_validator() -> None:
    date_schema = {
        "type": "object",
        "properties": {"event_time": {"type": "string", "format": "date-time"}},
    }
    data_valid = {"event_time": "2025-10-12T18:00:00Z"}
    data_invalid = {"event_time": "not a datetime"}  # Incorrect format

    validator = JSONSchemaValidator(schema=date_schema)
    assert validator(data_valid) == data_valid

    with pytest.raises(ValidationError):
        validator(data_invalid)

    other_validator = JSONSchemaValidator(schema=date_schema)
    assert validator == other_validator
    assert hash(validator) == hash(other_validator)
