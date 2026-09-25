from nautobot.apps.ui import (
    ButtonColorChoices,
    ObjectDetailContent,
    ObjectFieldsPanel,
    Panel,
    SectionChoices,
)
from nautobot.apps.views import NautobotUIViewSet
from nautobot.core.ui import object_detail

from nautobot_schedule import filters, forms, models, tables
from nautobot_schedule.api import serializers


class ScheduleTypeUIViewSet(NautobotUIViewSet):
    queryset = models.ScheduleType.objects.all()

    filterset_class = filters.ScheduleTypeFilterSet
    filterset_form_class = forms.ScheduleTypeFilterForm
    form_class = forms.ScheduleTypeForm
    serializer_class = serializers.ScheduleTypeSerializer
    table_class = tables.ScheduleTypeTable

    object_detail_content = ObjectDetailContent(
        panels=[
            ObjectFieldsPanel(
                weight=100,
                section=SectionChoices.LEFT_HALF,
                fields="__all__",
            ),
        ],
    )


class ScheduleUIViewSet(NautobotUIViewSet):
    queryset = models.Schedule.objects.all()

    filterset_class = filters.ScheduleFilterSet
    filterset_form_class = forms.ScheduleFilterForm
    form_class = forms.ScheduleForm
    serializer_class = serializers.ScheduleSerializer
    table_class = tables.ScheduleTable

    object_detail_content = ObjectDetailContent(
        panels=[
            ObjectFieldsPanel(
                weight=100,
                section=SectionChoices.RIGHT_HALF,
                fields="__all__",
            ),
            Panel(
                weight=200,
                section=SectionChoices.LEFT_HALF,
                body_content_template_path="nautobot_schedule/calendar.html",
            ),
        ],
        extra_buttons=[
            object_detail.Button(
                weight=100,
                color=ButtonColorChoices.BLUE,
                label="Add Event",
                icon="mdi-calendar-plus",
                link_name="plugins:nautobot_schedule:schedule_event_add",
            ),
        ],
    )


class RecurrenceRuleUIViewSet(NautobotUIViewSet):
    queryset = models.RecurrenceRule.objects.all()

    filterset_class = filters.RecurrenceRuleFilterSet
    filterset_form_class = forms.RecurrenceRuleFilterForm
    form_class = forms.RecurrenceRuleForm
    serializer_class = serializers.RecurrenceRuleSerializer
    table_class = tables.RecurrenceRuleTable

    object_detail_content = ObjectDetailContent(
        panels=[
            ObjectFieldsPanel(
                weight=100,
                section=SectionChoices.LEFT_HALF,
                fields="__all__",
            ),
        ],
    )


class EventUIViewSet(NautobotUIViewSet):
    queryset = models.Event.objects.all()

    filterset_class = filters.EventFilterSet
    filterset_form_class = forms.EventFilterForm
    form_class = forms.EventForm
    serializer_class = serializers.EventSerializer
    table_class = tables.EventTable

    object_detail_content = ObjectDetailContent(
        panels=[
            ObjectFieldsPanel(
                weight=100,
                section=SectionChoices.LEFT_HALF,
                fields="__all__",
                exclude_fields=("rdates",),
            ),
        ],
    )
