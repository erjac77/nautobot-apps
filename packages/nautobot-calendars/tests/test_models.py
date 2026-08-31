import datetime
from typing import Any

import pytest
from django.utils.dateparse import parse_datetime
from nautobot_calendars.factories import (
    CalendarFactory,
    CalendarTypeFactory,
    EventFactory,
    RecurrenceRuleFactory,
)
from nautobot_calendars.models import RecurrenceRule


def test_calendar(calendar_factory: CalendarFactory) -> None:
    calendar = calendar_factory.build(name="My calendar")
    assert str(calendar) == "My calendar"


def test_calendar_type(calendar_type_factory: CalendarTypeFactory) -> None:
    calendar_type = calendar_type_factory.build(name="My calendar type")
    assert str(calendar_type) == "My calendar type"


@pytest.mark.parametrize(
    ("kwargs", "dtstart", "expected"),
    [
        (
            {
                "name": "Daily, for 10 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.DAILY,
                "count": 10,
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-03T09:00:00Z"),
                parse_datetime("1997-09-04T09:00:00Z"),
                parse_datetime("1997-09-05T09:00:00Z"),
                parse_datetime("1997-09-06T09:00:00Z"),
                parse_datetime("1997-09-07T09:00:00Z"),
                parse_datetime("1997-09-08T09:00:00Z"),
                parse_datetime("1997-09-09T09:00:00Z"),
                parse_datetime("1997-09-10T09:00:00Z"),
                parse_datetime("1997-09-11T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Daily until Septembre 4, 1997",
                "freq": RecurrenceRule.FrequencyChoices.DAILY,
                "until": parse_datetime("1997-09-04T09:00:00Z"),
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-03T09:00:00Z"),
                parse_datetime("1997-09-04T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every other day, 5 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.DAILY,
                "interval": 2,
                "count": 5,
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-04T09:00:00Z"),
                parse_datetime("1997-09-06T09:00:00Z"),
                parse_datetime("1997-09-08T09:00:00Z"),
                parse_datetime("1997-09-10T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every 10 days, 5 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.DAILY,
                "interval": 10,
                "count": 5,
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-12T09:00:00Z"),
                parse_datetime("1997-09-22T09:00:00Z"),
                parse_datetime("1997-10-02T09:00:00Z"),
                parse_datetime("1997-10-12T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Weekly for 5 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.WEEKLY,
                "count": 5,
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-09T09:00:00Z"),
                parse_datetime("1997-09-16T09:00:00Z"),
                parse_datetime("1997-09-23T09:00:00Z"),
                parse_datetime("1997-09-30T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every other week, 5 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.WEEKLY,
                "interval": 2,
                "count": 5,
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-16T09:00:00Z"),
                parse_datetime("1997-09-30T09:00:00Z"),
                parse_datetime("1997-10-14T09:00:00Z"),
                parse_datetime("1997-10-28T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Weekly on Tuesday and Thursday for 2 weeks",
                "freq": RecurrenceRule.FrequencyChoices.WEEKLY,
                "count": 4,
                "wkst": RecurrenceRule.WeekdayChoices.SU,
                "byday": ["TU", "TH"],
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-04T09:00:00Z"),
                parse_datetime("1997-09-09T09:00:00Z"),
                parse_datetime("1997-09-11T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every other week on Tuesday and Thursday, for 4 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.WEEKLY,
                "interval": 2,
                "count": 4,
                "wkst": RecurrenceRule.WeekdayChoices.SU,
                "byday": ["TU", "TH"],
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-04T09:00:00Z"),
                parse_datetime("1997-09-16T09:00:00Z"),
                parse_datetime("1997-09-18T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Monthly on the 1st Friday for 5 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.MONTHLY,
                "count": 5,
                "byday": ["1FR"],
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-05T09:00:00Z"),
                parse_datetime("1997-10-03T09:00:00Z"),
                parse_datetime("1997-11-07T09:00:00Z"),
                parse_datetime("1997-12-05T09:00:00Z"),
                parse_datetime("1998-01-02T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every other month on the 1st and last Sunday of the month for 4 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.MONTHLY,
                "interval": 2,
                "count": 4,
                "byday": ["1SU", "-1SU"],
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-07T09:00:00Z"),
                parse_datetime("1997-09-28T09:00:00Z"),
                parse_datetime("1997-11-02T09:00:00Z"),
                parse_datetime("1997-11-30T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Monthly on the second to last Monday of the month for 6 months",
                "freq": RecurrenceRule.FrequencyChoices.MONTHLY,
                "count": 6,
                "byday": ["-2MO"],
            },
            parse_datetime("1997-09-22T09:00:00Z"),
            [
                parse_datetime("1997-09-22T09:00:00Z"),
                parse_datetime("1997-10-20T09:00:00Z"),
                parse_datetime("1997-11-17T09:00:00Z"),
                parse_datetime("1997-12-22T09:00:00Z"),
                parse_datetime("1998-01-19T09:00:00Z"),
                parse_datetime("1998-02-16T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Monthly on the third to the last day of the month, for 6 months",
                "freq": RecurrenceRule.FrequencyChoices.MONTHLY,
                "count": 6,
                "bymonthday": [-3],
            },
            parse_datetime("1997-09-28T09:00:00Z"),
            [
                parse_datetime("1997-09-28T09:00:00Z"),
                parse_datetime("1997-10-29T09:00:00Z"),
                parse_datetime("1997-11-28T09:00:00Z"),
                parse_datetime("1997-12-29T09:00:00Z"),
                parse_datetime("1998-01-29T09:00:00Z"),
                parse_datetime("1998-02-26T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Monthly on the 2nd and 15th of the month for 5 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.MONTHLY,
                "count": 5,
                "bymonthday": [2, 15],
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-15T09:00:00Z"),
                parse_datetime("1997-10-02T09:00:00Z"),
                parse_datetime("1997-10-15T09:00:00Z"),
                parse_datetime("1997-11-02T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Monthly on the first and last day of the month for 3 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.MONTHLY,
                "count": 5,
                "bymonthday": [-1, 1],
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-30T09:00:00Z"),
                parse_datetime("1997-10-01T09:00:00Z"),
                parse_datetime("1997-10-31T09:00:00Z"),
                parse_datetime("1997-11-01T09:00:00Z"),
                parse_datetime("1997-11-30T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every 18 months on the 10th thru 12th of the month for 5 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.MONTHLY,
                "interval": 18,
                "count": 5,
                "bymonthday": [10, 11, 12],
            },
            parse_datetime("1997-09-10T09:00:00Z"),
            [
                parse_datetime("1997-09-10T09:00:00Z"),
                parse_datetime("1997-09-11T09:00:00Z"),
                parse_datetime("1997-09-12T09:00:00Z"),
                parse_datetime("1999-03-10T09:00:00Z"),
                parse_datetime("1999-03-11T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every Tuesday, every other month, 6 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.MONTHLY,
                "interval": 2,
                "count": 6,
                "byday": ["TU"],
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-09T09:00:00Z"),
                parse_datetime("1997-09-16T09:00:00Z"),
                parse_datetime("1997-09-23T09:00:00Z"),
                parse_datetime("1997-09-30T09:00:00Z"),
                parse_datetime("1997-11-04T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Yearly in June and July for 4 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.YEARLY,
                "count": 4,
                "bymonth": [6, 7],
            },
            parse_datetime("1997-06-10T09:00:00Z"),
            [
                parse_datetime("1997-06-10T09:00:00Z"),
                parse_datetime("1997-07-10T09:00:00Z"),
                parse_datetime("1998-06-10T09:00:00Z"),
                parse_datetime("1998-07-10T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every 3rd year on the 1st, 100th and 200th day for 4 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.YEARLY,
                "interval": 3,
                "count": 4,
                "byyearday": [1, 100, 200],
            },
            parse_datetime("1997-01-01T09:00:00Z"),
            [
                parse_datetime("1997-01-01T09:00:00Z"),
                parse_datetime("1997-04-10T09:00:00Z"),
                parse_datetime("1997-07-19T09:00:00Z"),
                parse_datetime("2000-01-01T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every 20th Monday of the year, 3 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.YEARLY,
                "count": 3,
                "byday": ["20MO"],
            },
            parse_datetime("1997-05-19T09:00:00Z"),
            [
                parse_datetime("1997-05-19T09:00:00Z"),
                parse_datetime("1998-05-18T09:00:00Z"),
                parse_datetime("1999-05-17T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Monday of week number 20 (where the default start of the week is Monday), 3 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.YEARLY,
                "count": 3,
                "byweekno": 20,
                "byday": ["MO"],
            },
            parse_datetime("1997-05-12T09:00:00Z"),
            [
                parse_datetime("1997-05-12T09:00:00Z"),
                parse_datetime("1998-05-11T09:00:00Z"),
                parse_datetime("1999-05-17T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "The week number 1 may be in the last year",
                "freq": RecurrenceRule.FrequencyChoices.YEARLY,
                "count": 3,
                "byweekno": 1,
                "byday": ["MO"],
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-12-29T09:00:00Z"),
                parse_datetime("1999-01-04T09:00:00Z"),
                parse_datetime("2000-01-03T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "And the week numbers greater than 51 may be in the next year",
                "freq": RecurrenceRule.FrequencyChoices.YEARLY,
                "count": 3,
                "byweekno": 52,
                "byday": ["SU"],
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-12-28T09:00:00Z"),
                parse_datetime("1998-12-27T09:00:00Z"),
                parse_datetime("2000-01-02T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Only some years have week number 53",
                "freq": RecurrenceRule.FrequencyChoices.YEARLY,
                "count": 3,
                "byweekno": 53,
                "byday": ["MO"],
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1998-12-28T09:00:00Z"),
                parse_datetime("2004-12-27T09:00:00Z"),
                parse_datetime("2009-12-28T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every Friday the 13th, 4 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.YEARLY,
                "count": 4,
                "byday": ["FR"],
                "bymonthday": [13],
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1998-02-13T09:00:00Z"),
                parse_datetime("1998-03-13T09:00:00Z"),
                parse_datetime("1998-11-13T09:00:00Z"),
                parse_datetime("1999-08-13T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every four years, the first Tuesday after a Monday in November, 3 occurrences (U.S. Presidential Election day)",
                "freq": RecurrenceRule.FrequencyChoices.YEARLY,
                "interval": 4,
                "count": 3,
                "bymonth": 11,
                "byday": ["TU"],
                "bymonthday": [2, 3, 4, 5, 6, 7, 8],
            },
            parse_datetime("1996-11-05T09:00:00Z"),
            [
                parse_datetime("1996-11-05T09:00:00Z"),
                parse_datetime("2000-11-07T09:00:00Z"),
                parse_datetime("2004-11-02T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "The 3rd instance into the month of one of Tuesday, Wednesday or Thursday, for the next 3 months",
                "freq": RecurrenceRule.FrequencyChoices.MONTHLY,
                "count": 3,
                "byday": ["TU", "WE", "TH"],
                "bysetpos": [3],
            },
            parse_datetime("1997-09-04T09:00:00Z"),
            [
                parse_datetime("1997-09-04T09:00:00Z"),
                parse_datetime("1997-10-07T09:00:00Z"),
                parse_datetime("1997-11-06T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "The 2nd to last weekday of the month, 3 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.MONTHLY,
                "count": 3,
                "byday": ["MO", "TU", "WE", "TH", "FR"],
                "bysetpos": [-2],
            },
            parse_datetime("1997-09-29T09:00:00Z"),
            [
                parse_datetime("1997-09-29T09:00:00Z"),
                parse_datetime("1997-10-30T09:00:00Z"),
                parse_datetime("1997-11-27T09:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every 3 hours from 9:00 AM to 5:00 PM on a specific day",
                "freq": RecurrenceRule.FrequencyChoices.HOURLY,
                "interval": 3,
                "until": parse_datetime("1997-09-02T17:00:00Z"),
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-02T12:00:00Z"),
                parse_datetime("1997-09-02T15:00:00Z"),
            ],
        ),
        (
            {
                "name": "Every 15 minutes for 6 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.MINUTELY,
                "interval": 15,
                "count": 6,
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-02T09:15:00Z"),
                parse_datetime("1997-09-02T09:30:00Z"),
                parse_datetime("1997-09-02T09:45:00Z"),
                parse_datetime("1997-09-02T10:00:00Z"),
                parse_datetime("1997-09-02T10:15:00Z"),
            ],
        ),
        (
            {
                "name": "Every hour and a half for 4 occurrences",
                "freq": RecurrenceRule.FrequencyChoices.MINUTELY,
                "interval": 90,
                "count": 4,
            },
            parse_datetime("1997-09-02T09:00:00Z"),
            [
                parse_datetime("1997-09-02T09:00:00Z"),
                parse_datetime("1997-09-02T10:30:00Z"),
                parse_datetime("1997-09-02T12:00:00Z"),
                parse_datetime("1997-09-02T13:30:00Z"),
            ],
        ),
    ],
)
def test_recurrent_rule(
    recurrence_rule_factory: RecurrenceRuleFactory,
    kwargs: dict[str, Any],
    dtstart: datetime.datetime,
    expected: list[datetime.datetime],
) -> None:
    recurrence_rule = recurrence_rule_factory.build(**kwargs)
    recur = recurrence_rule.to_dateutil_rrule(dtstart=dtstart)
    assert str(recurrence_rule) == kwargs["name"]
    assert list(recur) == expected


def test_event(event_factory: EventFactory) -> None:
    event = event_factory.build(
        title="My Event",
        dtstart=parse_datetime("1997-09-02T09:00:00Z"),
        dtend=parse_datetime("1997-09-02T10:00:00Z"),
    )
    assert str(event) == "My Event"
    assert event.duration == datetime.timedelta(hours=1)
    assert event.recurrences(
        after=parse_datetime("1997-09-02T09:00:00Z"),
        before=parse_datetime("1997-09-02T10:00:00Z"),
    ) == [
        parse_datetime("1997-09-02T09:00:00Z"),
    ]
    assert (
        event.recurrences(
            after=parse_datetime("1997-09-02T09:00:00Z"),
            before=parse_datetime("1997-09-02T10:00:00Z"),
            inc=False,
        )
        == []
    )
    assert event.intersect(
        dtstart=parse_datetime("1997-09-02T09:30:00Z"),
        dtend=parse_datetime("1997-09-02T10:30:00Z"),
    )
    assert not event.intersect(
        dtstart=parse_datetime("1997-09-02T10:30:00Z"),
        dtend=parse_datetime("1997-09-02T11:30:00Z"),
    )


@pytest.mark.django_db
def test_recurrent_events(
    event_factory: EventFactory,
    recurrence_rule_factory: RecurrenceRuleFactory,
) -> None:
    recurrence_rule = recurrence_rule_factory.create(
        name="Daily, for 5 occurrences",
        freq=RecurrenceRule.FrequencyChoices.DAILY,
        count=5,
    )
    recurrence_rule.full_clean()

    event = event_factory.create(
        title="My Event",
        dtstart=parse_datetime("1997-09-02T09:00:00Z"),
        dtend=parse_datetime("1997-09-02T10:00:00Z"),
        recurrence_rule=recurrence_rule,
        exdates=["1997-09-03T09:00:00Z"],
        rdates=["1997-09-08T09:00:00Z", "1997-10-03T09:00:00Z"],
    )
    assert str(event) == "My Event"
    assert event.duration == datetime.timedelta(hours=1)
    assert event.recurrences(
        after=parse_datetime("1997-09-04T09:00:00Z"),
        before=parse_datetime("1997-09-08T09:00:00Z"),
    ) == [
        parse_datetime("1997-09-04T09:00:00Z"),
        parse_datetime("1997-09-05T09:00:00Z"),
        parse_datetime("1997-09-06T09:00:00Z"),
        parse_datetime("1997-09-08T09:00:00Z"),
    ]
    assert event.recurrences(
        after=parse_datetime("1997-09-04T09:00:00Z"),
        before=parse_datetime("1997-09-06T09:00:00Z"),
        inc=False,
    ) == [
        parse_datetime("1997-09-05T09:00:00Z"),
    ]
    assert (
        event.recurrences(
            after=parse_datetime("1997-09-05T09:00:00Z"),
            before=parse_datetime("1997-09-06T09:00:00Z"),
            inc=False,
        )
        == []
    )
    assert event.intersect(
        dtstart=parse_datetime("1997-09-04T09:30:00Z"),
        dtend=parse_datetime("1997-09-04T10:30:00Z"),
    )
    assert not event.intersect(
        dtstart=parse_datetime("1997-09-04T10:30:00Z"),
        dtend=parse_datetime("1997-09-04T11:30:00Z"),
    )
