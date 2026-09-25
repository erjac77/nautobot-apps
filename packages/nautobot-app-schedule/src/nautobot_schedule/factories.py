from datetime import timedelta

from django.utils import timezone
from factory import LazyAttribute, Sequence, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from nautobot_schedule.models import Event, RecurrenceRule, Schedule, ScheduleType


class ScheduleTypeFactory(DjangoModelFactory[ScheduleType]):
    class Meta:
        model = ScheduleType

    name = Sequence(lambda n: f"Schedule Type {n}")


class ScheduleFactory(DjangoModelFactory[Schedule]):
    class Meta:
        model = Schedule

    schedule_type = SubFactory(ScheduleTypeFactory)

    name = Sequence(lambda n: f"Schedule {n}")


class RecurrenceRuleFactory(DjangoModelFactory[RecurrenceRule]):
    class Meta:
        model = RecurrenceRule

    name = Sequence(lambda n: f"Recurrence Rule {n}")
    freq = fuzzy.FuzzyChoice(choices=RecurrenceRule.FrequencyChoices)


class EventFactory(DjangoModelFactory[Event]):
    class Meta:
        model = Event

    schedule = SubFactory(ScheduleFactory)

    title = Sequence(lambda n: f"Event {n}")
    dtstart = fuzzy.FuzzyDateTime(
        start_dt=timezone.now(), force_minute=0, force_second=0, force_microsecond=0
    )
    dtend = LazyAttribute(lambda self: self.dtstart + timedelta(hours=1))
