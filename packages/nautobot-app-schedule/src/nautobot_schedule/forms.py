from django import forms
from nautobot.apps.forms import (
    DateTimePicker,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    NautobotFilterForm,
    NautobotModelForm,
)

from nautobot_schedule import models


class ScheduleTypeForm(NautobotModelForm):
    class Meta:
        model = models.ScheduleType
        fields = "__all__"


class ScheduleTypeFilterForm(NautobotFilterForm):
    model = models.ScheduleType

    q = forms.CharField(required=False, label="Search")


class ScheduleForm(NautobotModelForm):
    schedule_type = DynamicModelChoiceField(
        queryset=models.ScheduleType.objects.all(), required=False, label="Schedule Type"
    )

    class Meta:
        model = models.Schedule
        fields = "__all__"


class ScheduleFilterForm(NautobotFilterForm):
    model = models.Schedule
    q = forms.CharField(required=False, label="Search")
    schedule_type = DynamicModelMultipleChoiceField(
        queryset=models.ScheduleType.objects.all(),
        to_field_name="name",
        required=False,
        label="Schedule Type",
    )


class RecurrenceRuleForm(NautobotModelForm):
    class Meta:
        model = models.RecurrenceRule
        fields = "__all__"

        widgets = {  # noqa: RUF012
            "until": DateTimePicker(attrs={"placeholder": "YYYY-MM-DD HH:MM:SS"}),
        }


class RecurrenceRuleFilterForm(NautobotFilterForm):
    model = models.RecurrenceRule
    q = forms.CharField(required=False, label="Search")


class EventForm(NautobotModelForm):
    schedule = DynamicModelChoiceField(queryset=models.Schedule.objects.all(), label="Schedule")
    recurrence_rule = DynamicModelChoiceField(
        queryset=models.RecurrenceRule.objects.all(), required=False, label="Recurrence Rule"
    )

    class Meta:
        model = models.Event
        fields = "__all__"
        exclude = ("rdates",)

        widgets = {  # noqa: RUF012
            "dtstart": DateTimePicker(attrs={"placeholder": "YYYY-MM-DD HH:MM:SS"}),
            "dtend": DateTimePicker(attrs={"placeholder": "YYYY-MM-DD HH:MM:SS"}),
        }


class EventFilterForm(NautobotFilterForm):
    model = models.Event
    q = forms.CharField(required=False, label="Search")
    schedule = DynamicModelMultipleChoiceField(
        queryset=models.Schedule.objects.all(),
        to_field_name="name",
        required=False,
        label="Schedule",
    )
    recurrence_rule = DynamicModelMultipleChoiceField(
        queryset=models.RecurrenceRule.objects.all(),
        to_field_name="name",
        required=False,
        label="Recurrence Rule",
    )
