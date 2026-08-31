import json
from typing import Any

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from jsonschema import FormatChecker, validate
from jsonschema.exceptions import ValidationError as JSONSchemaValidationError


@deconstructible
class JSONSchemaValidator:
    """Django JSONField validator using jsonschema."""

    def __init__(self, schema: dict[str, Any]) -> None:
        self.schema = schema

    def __call__(self, instance: object) -> object:
        """Validates an instance under the given schema."""
        try:
            validate(instance, self.schema, format_checker=FormatChecker())
        except JSONSchemaValidationError as err:
            raise ValidationError(err.message) from err

        return instance

    def __eq__(self, other: object) -> bool:
        """Returns True if both instances have the same schema."""
        return isinstance(other, JSONSchemaValidator) and self.schema == other.schema

    def __hash__(self) -> int:
        """Returns the hash of the schema."""
        return hash(json.dumps(self.schema, sort_keys=True))
