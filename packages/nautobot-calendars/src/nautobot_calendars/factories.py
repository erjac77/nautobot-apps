from datetime import timedelta

from django.utils import timezone
from factory import LazyAttribute, Sequence, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from nautobot_calendars.models import Calendar, CalendarType, Event, RecurrenceRule


class CalendarTypeFactory(DjangoModelFactory[CalendarType]):
    class Meta:
        model = CalendarType

    name = Sequence(lambda n: f"Calendar Type {n}")


class CalendarFactory(DjangoModelFactory[Calendar]):
    class Meta:
        model = Calendar

    calendar_type = SubFactory(CalendarTypeFactory)

    name = Sequence(lambda n: f"Calendar {n}")


class RecurrenceRuleFactory(DjangoModelFactory[RecurrenceRule]):
    class Meta:
        model = RecurrenceRule

    name = Sequence(lambda n: f"Recurrence Rule {n}")
    freq = fuzzy.FuzzyChoice(choices=RecurrenceRule.FrequencyChoices)


class EventFactory(DjangoModelFactory[Event]):
    class Meta:
        model = Event

    calendar = SubFactory(CalendarFactory)

    title = Sequence(lambda n: f"Event {n}")
    dtstart = fuzzy.FuzzyDateTime(
        start_dt=timezone.now(), force_minute=0, force_second=0, force_microsecond=0
    )
    dtend = LazyAttribute(lambda self: self.dtstart + timedelta(hours=1))
