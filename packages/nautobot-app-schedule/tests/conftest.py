from nautobot_schedule.factories import (
    EventFactory,
    RecurrenceRuleFactory,
    ScheduleFactory,
    ScheduleTypeFactory,
)
from pytest_factoryboy import register


register(ScheduleFactory)
register(ScheduleTypeFactory)
register(EventFactory)
register(RecurrenceRuleFactory)
