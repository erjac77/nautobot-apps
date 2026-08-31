from typing import Any

from nautobot.apps.api import NautobotModelSerializer
from rest_framework import serializers

from nautobot_calendars.models import Calendar, CalendarType, Event, RecurrenceRule


class RecurrenceRuleSerializer(NautobotModelSerializer):
    class Meta:
        model = RecurrenceRule
        fields = "__all__"


class EventSerializer(serializers.HyperlinkedModelSerializer):
    start = serializers.DateTimeField(source="dtstart")
    end = serializers.DateTimeField(source="dtend")
    rrule = serializers.SerializerMethodField()
    duration = serializers.DurationField(read_only=True)
    exdate = serializers.ListField(
        child=serializers.DateTimeField(),
        source="exdates",
        required=False,
    )
    rdate = serializers.ListField(
        child=serializers.DateTimeField(),
        source="rdates",
        required=False,
    )

    class Meta:
        model = Event
        fields = ("id", "title", "start", "end", "rrule", "duration", "exdate", "rdate")

    def to_representation(self, instance: Event) -> dict[str, Any]:
        """Override the default to_representation to exclude the rrule fields."""
        representation = super().to_representation(instance)
        if instance.recurrence_rule is None:
            representation.pop("rrule")
            representation.pop("duration")
            representation.pop("exdate")
            representation.pop("rdate")
        else:
            representation.pop("start")
            representation.pop("end")
        return representation

    def get_rrule(self, obj: Event) -> str:
        if obj.recurrence_rule is None:
            return ""
        return str(obj.recurrence_rule.to_dateutil_rrule(dtstart=obj.dtstart))


class CalendarTypeSerializer(NautobotModelSerializer):
    class Meta:
        model = CalendarType
        fields = "__all__"


class RangeSerializer(serializers.Serializer):
    """API Serializer to validate range query string parameters."""

    start = serializers.DateTimeField(required=True)
    end = serializers.DateTimeField(required=True)


class CalendarSerializer(NautobotModelSerializer):
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Calendar
        fields = ("id", "name", "description", "events")


class RecurrentEventSerializer(serializers.Serializer[Any]):
    """API Serializer to validate query string parameters for recurrent event."""

    after = serializers.DateTimeField(required=True)
    before = serializers.DateTimeField(required=True)
