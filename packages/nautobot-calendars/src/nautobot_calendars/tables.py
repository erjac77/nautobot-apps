import django_tables2 as tables
from nautobot.apps.tables import BaseTable, ButtonsColumn, ToggleColumn

from nautobot_calendars import models


class CalendarTypeTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn()
    actions = ButtonsColumn(models.CalendarType)

    class Meta(BaseTable.Meta):
        model = models.CalendarType
        fields = ("pk", "name", "description")
        default_columns = ("pk", "name", "description")


class CalendarTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn()
    calendar_type = tables.LinkColumn()
    actions = ButtonsColumn(models.Calendar)

    class Meta(BaseTable.Meta):
        model = models.Calendar
        fields = ("pk", "name", "description", "calendar_type")
        default_columns = ("pk", "name", "description", "calendar_type")


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
    calendar = tables.LinkColumn()
    recurrence_rule = tables.LinkColumn()
    actions = ButtonsColumn(models.Event)

    class Meta(BaseTable.Meta):
        model = models.Event
        fields = ("pk", "title", "description", "calendar", "dtstart", "dtend", "recurrence_rule")
        default_columns = (
            "pk",
            "title",
            "description",
            "calendar",
            "dtstart",
            "dtend",
            "recurrence_rule",
        )
