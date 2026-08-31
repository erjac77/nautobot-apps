from django import forms
from nautobot.apps.forms import (
    DateTimePicker,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    NautobotFilterForm,
    NautobotModelForm,
)

from nautobot_calendars import models


class CalendarTypeForm(NautobotModelForm):
    class Meta:
        model = models.CalendarType
        fields = "__all__"


class CalendarTypeFilterForm(NautobotFilterForm):
    model = models.CalendarType
    q = forms.CharField(required=False, label="Search")


class CalendarForm(NautobotModelForm):
    calendar_type = DynamicModelChoiceField(
        queryset=models.CalendarType.objects.all(), required=False, label="Calendar Type"
    )

    class Meta:
        model = models.Calendar
        fields = "__all__"


class CalendarFilterForm(NautobotFilterForm):
    model = models.Calendar
    q = forms.CharField(required=False, label="Search")
    calendar_type = DynamicModelMultipleChoiceField(
        queryset=models.CalendarType.objects.all(),
        to_field_name="name",
        required=False,
        label="Calendar Type",
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
    calendar = DynamicModelChoiceField(
        queryset=models.Calendar.objects.all(), required=False, label="Calendar"
    )
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
    model = models.Calendar
    q = forms.CharField(required=False, label="Search")
    calendar = DynamicModelMultipleChoiceField(
        queryset=models.Calendar.objects.all(),
        to_field_name="name",
        required=False,
        label="Calendar",
    )
    recurrence_rule = DynamicModelMultipleChoiceField(
        queryset=models.RecurrenceRule.objects.all(),
        to_field_name="name",
        required=False,
        label="Recurrence Rule",
    )
