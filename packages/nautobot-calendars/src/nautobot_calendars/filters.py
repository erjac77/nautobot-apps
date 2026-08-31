from datetime import datetime

import django_filters
from django.db.models import QuerySet
from nautobot.core.filters import (
    NaturalKeyOrPKMultipleChoiceFilter,
    SearchFilter,
)
from nautobot.extras.filters import NautobotFilterSet

from nautobot_calendars import models


class CalendarTypeFilterSet(NautobotFilterSet):
    q = SearchFilter(
        filter_predicates={"name": "icontains", "description": "icontains"},
    )

    class Meta:
        model = models.CalendarType
        fields = "__all__"


class CalendarFilterSet(NautobotFilterSet):
    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "description": "icontains",
            "calendar_type__name": "icontains",
        },
    )

    calendar_type = NaturalKeyOrPKMultipleChoiceFilter(
        queryset=models.CalendarType.objects.all(),
        to_field_name="name",
        label="Calendar Type (name or ID)",
    )
    start = django_filters.DateTimeFilter(method="dummy")
    end = django_filters.DateTimeFilter(method="dummy")

    class Meta:
        model = models.Calendar
        fields = "__all__"

    def dummy(
        self,
        queryset: QuerySet[models.Calendar],
        name: str,  # noqa: ARG002
        value: datetime,  # noqa: ARG002
    ) -> QuerySet[models.Calendar]:
        """Dummy method to satisfy the presence of the `start` and `end` filters.

        The actual filtering by date range is handled in the view method itself,
        so this method just returns the unfiltered queryset.
        """
        return queryset


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
            "calendar__name": "icontains",
        },
    )

    calendar = NaturalKeyOrPKMultipleChoiceFilter(
        queryset=models.Calendar.objects.all(), to_field_name="name", label="Calendar (name or ID)"
    )
    recurrence_rule = NaturalKeyOrPKMultipleChoiceFilter(
        queryset=models.RecurrenceRule.objects.all(),
        to_field_name="name",
        label="Recurrence Rule (name or ID)",
    )
    after = django_filters.DateTimeFilter(method="dummy")
    before = django_filters.DateTimeFilter(method="dummy")

    class Meta:
        model = models.Event
        fields = "__all__"

    def dummy(
        self,
        queryset: QuerySet[models.Event],
        name: str,  # noqa: ARG002
        value: datetime,  # noqa: ARG002
    ) -> QuerySet[models.Event]:
        """Dummy method to satisfy the presence of the `after` and `before` filters.

        The actual filtering by date range is handled in the view method itself,
        so this method just returns the unfiltered queryset.
        """
        return queryset
