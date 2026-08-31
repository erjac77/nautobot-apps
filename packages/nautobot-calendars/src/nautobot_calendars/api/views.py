from uuid import UUID

from nautobot.apps.api import NautobotModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from nautobot_calendars import filters, models
from nautobot_calendars.api import serializers


class CalendarTypeViewSet(NautobotModelViewSet):
    queryset = models.CalendarType.objects.all()
    serializer_class = serializers.CalendarTypeSerializer
    filterset_class = filters.CalendarTypeFilterSet


class CalendarViewSet(NautobotModelViewSet):
    queryset = models.Calendar.objects.all()
    serializer_class = serializers.CalendarSerializer
    filterset_class = filters.CalendarFilterSet

    @action(detail=True, methods=["GET"])
    def events(self, request: Request, pk: UUID) -> Response:  # noqa: ARG002
        """Returns a list of events for this calendar.

        The `start` and `end` query parameters are required and must be ISO 8601
        datetimes. Only events that intersect the given time range will be returned.
        """
        serializer = serializers.RangeSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        start = serializer.validated_data["start"]
        end = serializer.validated_data["end"]

        calendar = self.get_object()
        events = calendar.events.all()
        ids = [evt.id for evt in events if evt.intersect(start, end)]
        serializer = serializers.EventSerializer(
            events.filter(id__in=ids),
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)


class RecurrenceRuleViewSet(NautobotModelViewSet):
    """API viewset for interacting with recurrence rule objects."""

    queryset = models.RecurrenceRule.objects.all()
    serializer_class = serializers.RecurrenceRuleSerializer
    filterset_class = filters.RecurrenceRuleFilterSet


class EventViewSet(NautobotModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filterset_class = filters.EventFilterSet

    @action(detail=True, methods=["GET"])
    def recurrences(self, request: Request, pk: UUID) -> Response:  # noqa: ARG002
        """Returns a list of recurrences for this event.

        The `after` and `before` query parameters are used to bound the recurrence
        generation window. Both should be ISO 8601 datetimes.
        """
        evt_ser = serializers.RecurrentEventSerializer(data=request.query_params)
        evt_ser.is_valid(raise_exception=True)
        validated_params = evt_ser.validated_data
        event = self.get_object()
        return Response(
            list(
                event.recurrences(
                    validated_params.get("after"),
                    validated_params.get("before"),
                ),
            ),
        )
