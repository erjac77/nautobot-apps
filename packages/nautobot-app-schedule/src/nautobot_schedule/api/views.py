from uuid import UUID

from nautobot.apps.api import NautobotModelViewSet
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from nautobot_schedule import filters, models
from nautobot_schedule.api import serializers


class ScheduleTypeViewSet(NautobotModelViewSet):
    queryset = models.ScheduleType.objects.all()

    filterset_class = filters.ScheduleTypeFilterSet
    serializer_class = serializers.ScheduleTypeSerializer


class ScheduleViewSet(NautobotModelViewSet):
    queryset = models.Schedule.objects.all()

    filterset_class = filters.ScheduleFilterSet
    serializer_class = serializers.ScheduleSerializer

    @action(detail=True, filterset_class=filters.DateTimeRangeFilterSet, methods=["GET"])
    def events(self, request: Request, pk: UUID) -> Response:  # noqa: ARG002
        """Returns a list of events for this schedule.

        The `start` and `end` query parameters are required and must be ISO 8601
        datetimes. Only events that intersect the given time range will be returned.
        """
        serializer = serializers.DateTimeRangeSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        start = serializer.validated_data["start"]
        end = serializer.validated_data["end"]

        schedule = self.get_object()
        events = schedule.events.all()
        ids = [evt.id for evt in events if evt.intersect(start, end)]
        serializer = serializers.EventSerializer(
            events.filter(id__in=ids), many=True, context={"request": request}
        )
        return Response(serializer.data)


class RecurrenceRuleViewSet(NautobotModelViewSet):
    """API viewset for interacting with recurrence rule objects."""

    queryset = models.RecurrenceRule.objects.all()

    filterset_class = filters.RecurrenceRuleFilterSet
    serializer_class = serializers.RecurrenceRuleSerializer


class EventViewSet(NautobotModelViewSet):
    queryset = models.Event.objects.all()

    filterset_class = filters.EventFilterSet
    serializer_class = serializers.EventSerializer

    @action(detail=True, filterset_class=filters.DateTimeRangeFilterSet, methods=["GET"])
    def recurrences(self, request: Request, pk: UUID) -> Response:  # noqa: ARG002
        """Returns a list of recurrences for this event.

        The `start` and `end` query parameters are used to bound the recurrence
        generation window. Both should be ISO 8601 datetimes.
        """
        evt_ser = serializers.DateTimeRangeSerializer(data=request.query_params)
        evt_ser.is_valid(raise_exception=True)
        validated_params = evt_ser.validated_data
        event = self.get_object()
        return Response(
            list(
                event.recurrences(
                    after=validated_params.get("start"), before=validated_params.get("end")
                )
            )
        )
