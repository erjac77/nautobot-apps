import django_tables2 as tables
from nautobot.apps.tables import BaseTable, ButtonsColumn, ToggleColumn

from nautobot_schedule import models


class ScheduleTypeTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn()
    actions = ButtonsColumn(models.ScheduleType)

    class Meta(BaseTable.Meta):
        model = models.ScheduleType
        fields = ("pk", "name", "description")
        default_columns = ("pk", "name", "description")


class ScheduleTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn()
    schedule_type = tables.LinkColumn()
    actions = ButtonsColumn(models.Schedule)

    class Meta(BaseTable.Meta):
        model = models.Schedule
        fields = ("pk", "name", "description", "schedule_type")
        default_columns = ("pk", "name", "description", "schedule_type")


class RecurrenceRuleTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn()
    actions = ButtonsColumn(models.RecurrenceRule)

    class Meta(BaseTable.Meta):
        model = models.RecurrenceRule
        fields = ("pk", "name", "description")
        default_columns = ("pk", "name", "description")


class EventTable(BaseTable):
    pk = ToggleColumn()
    title = tables.LinkColumn()
    schedule = tables.LinkColumn()
    recurrence_rule = tables.LinkColumn()
    actions = ButtonsColumn(models.Event)

    class Meta(BaseTable.Meta):
        model = models.Event
        fields = ("pk", "title", "description", "schedule", "dtstart", "dtend", "recurrence_rule")
        default_columns = (
            "pk",
            "title",
            "description",
            "schedule",
            "dtstart",
            "dtend",
            "recurrence_rule",
        )
