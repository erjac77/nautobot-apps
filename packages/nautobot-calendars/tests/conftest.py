from nautobot_calendars.factories import (
    CalendarFactory,
    CalendarTypeFactory,
    EventFactory,
    RecurrenceRuleFactory,
)
from pytest_factoryboy import register


register(CalendarFactory)
register(CalendarTypeFactory)
register(EventFactory)
register(RecurrenceRuleFactory)
