from datetime import datetime

import django_filters
from django.db.models import QuerySet
from nautobot.core.filters import (
    NaturalKeyOrPKMultipleChoiceFilter,
    SearchFilter,
)
from nautobot.extras.filters import NautobotFilterSet

from nautobot_schedule import models


class ScheduleTypeFilterSet(NautobotFilterSet):
    q = SearchFilter(
        filter_predicates={"name": "icontains", "description": "icontains"},
    )

    class Meta:
        model = models.ScheduleType
        fields = "__all__"


class ScheduleFilterSet(NautobotFilterSet):
    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "description": "icontains",
            "schedule_type__name": "icontains",
        },
    )

    schedule_type = NaturalKeyOrPKMultipleChoiceFilter(
        queryset=models.ScheduleType.objects.all(),
        to_field_name="name",
        label="Schedule Type (name or ID)",
    )

    class Meta:
        model = models.Schedule
        fields = "__all__"


class RecurrenceRuleFilterSet(NautobotFilterSet):
    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "description": "icontains",
            "event__title": "icontains",
        },
    )

    event = NaturalKeyOrPKMultipleChoiceFilter(
        queryset=models.Event.objects.all(), to_field_name="title", label="Event (title or ID)"
    )

    class Meta:
        model = models.RecurrenceRule
        fields = "__all__"


class EventFilterSet(NautobotFilterSet):
    q = SearchFilter(
        filter_predicates={
            "title": "icontains",
            "description": "icontains",
            "schedule__name": "icontains",
        },
    )

    schedule = NaturalKeyOrPKMultipleChoiceFilter(
        queryset=models.Schedule.objects.all(), to_field_name="name", label="Schedule (name or ID)"
    )
    recurrence_rule = NaturalKeyOrPKMultipleChoiceFilter(
        queryset=models.RecurrenceRule.objects.all(),
        to_field_name="name",
        label="Recurrence Rule (name or ID)",
    )

    class Meta:
        model = models.Event
        fields = "__all__"


class DateTimeRangeFilterSet(django_filters.FilterSet):
    start = django_filters.DateTimeFilter(label="Start", method="dummy")
    end = django_filters.DateTimeFilter(label="End", method="dummy")

    def dummy(
        self,
        queryset: QuerySet[models.Event],
        name: str,  # noqa: ARG002
        value: datetime,  # noqa: ARG002
    ) -> QuerySet[models.Event]:
        """Dummy method to satisfy the presence of the `start` and `end` filters.

        The actual filtering by date range is handled in the view method itself,
        so this method just returns the unfiltered queryset.
        """
        return queryset
