from nautobot.apps import ui, views
from nautobot.core.ui import object_detail

from nautobot_calendars import filters, forms, models, tables
from nautobot_calendars.api import serializers


class CalendarTypeUIViewSet(views.NautobotUIViewSet):
    filterset_class = filters.CalendarTypeFilterSet
    filterset_form_class = forms.CalendarTypeFilterForm
    form_class = forms.CalendarTypeForm
    queryset = models.CalendarType.objects.all()
    serializer_class = serializers.CalendarTypeSerializer
    table_class = tables.CalendarTypeTable

    object_detail_content = ui.ObjectDetailContent(
        panels=[
            ui.ObjectFieldsPanel(
                weight=100,
                section=ui.SectionChoices.LEFT_HALF,
                fields="__all__",
            ),
        ],
    )


class CalendarUIViewSet(views.NautobotUIViewSet):
    filterset_class = filters.CalendarFilterSet
    filterset_form_class = forms.CalendarFilterForm
    form_class = forms.CalendarForm
    queryset = models.Calendar.objects.all()
    serializer_class = serializers.CalendarSerializer
    table_class = tables.CalendarTable

    object_detail_content = ui.ObjectDetailContent(
        panels=[
            ui.ObjectFieldsPanel(
                weight=100,
                section=ui.SectionChoices.RIGHT_HALF,
                fields="__all__",
            ),
            ui.Panel(
                weight=200,
                section=ui.SectionChoices.LEFT_HALF,
                body_content_template_path="nautobot_calendars/calendar.html",
            ),
        ],
        extra_buttons=[
            object_detail.Button(
                weight=100,
                color=ui.ButtonColorChoices.BLUE,
                label="Add Event",
                icon="mdi-calendar-plus",
                link_name="plugins:nautobot_calendars:calendar_event_add",
            ),
        ],
    )


class RecurrenceRuleUIViewSet(views.NautobotUIViewSet):
    filterset_class = filters.RecurrenceRuleFilterSet
    filterset_form_class = forms.RecurrenceRuleFilterForm
    form_class = forms.RecurrenceRuleForm
    queryset = models.RecurrenceRule.objects.all()
    serializer_class = serializers.RecurrenceRuleSerializer
    table_class = tables.RecurrenceRuleTable

    object_detail_content = ui.ObjectDetailContent(
        panels=[
            ui.ObjectFieldsPanel(
                weight=100,
                section=ui.SectionChoices.LEFT_HALF,
                fields="__all__",
            ),
        ],
    )


class EventUIViewSet(views.NautobotUIViewSet):
    filterset_class = filters.EventFilterSet
    filterset_form_class = forms.EventFilterForm
    form_class = forms.EventForm
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    table_class = tables.EventTable

    object_detail_content = ui.ObjectDetailContent(
        panels=[
            ui.ObjectFieldsPanel(
                weight=100,
                section=ui.SectionChoices.LEFT_HALF,
                fields="__all__",
                exclude_fields=("rdates",),
            ),
        ],
    )
