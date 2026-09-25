import pytest
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from nautobot_schedule.factories import EventFactory, RecurrenceRuleFactory, ScheduleFactory
from nautobot_schedule.models import RecurrenceRule
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_given_logged_in_user_when_access_schedule_events_see_recurring_events(
    api_client_with_credentials: APIClient,
    schedule_factory: ScheduleFactory,
    event_factory: EventFactory,
    recurrence_rule_factory: RecurrenceRuleFactory,
) -> None:
    schedule = schedule_factory.create(name="My Schdule")
    recurrence_rule = recurrence_rule_factory.create(
        name="Daily, for 5 occurrences",
        freq=RecurrenceRule.FrequencyChoices.WEEKLY,
        count=5,
    )
    event_factory.create(
        schedule=schedule,
        title="My included Event",
        dtstart=parse_datetime("1997-09-02T09:00:00Z"),
        dtend=parse_datetime("1997-09-02T10:00:00Z"),
    )
    event_factory.create(
        schedule=schedule,
        title="My included recurring Event",
        dtstart=parse_datetime("1997-08-15T09:00:00Z"),
        dtend=parse_datetime("1997-08-15T10:00:00Z"),
        recurrence_rule=recurrence_rule,
    )
    event_factory.create(
        schedule=schedule,
        title="My excluded Event",
        dtstart=parse_datetime("1997-10-02T09:00:00Z"),
        dtend=parse_datetime("1997-10-02T10:00:00Z"),
    )
    url = reverse(
        "plugins-api:nautobot_schedule-api:schedule-events",
        kwargs={"pk": schedule.id},
    )
    response = api_client_with_credentials.get(
        url,
        data={
            "start": "1997-09-01T00:00:00Z",
            "end": "1997-09-30T00:00:00Z",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    titles = [d["title"] for d in data]
    assert "My included Event" in titles
    assert "My included recurring Event" in titles
    assert "My excluded Event" not in titles


@pytest.mark.django_db
def test_given_logged_in_user_when_access_event_recurrences_then_see_recurrences(
    api_client_with_credentials: APIClient,
    event_factory: EventFactory,
    recurrence_rule_factory: RecurrenceRuleFactory,
) -> None:
    recurrence_rule = recurrence_rule_factory.create(
        name="Daily, for 5 occurrences",
        freq=RecurrenceRule.FrequencyChoices.DAILY,
        count=5,
    )
    event = event_factory.create(
        title="My Event",
        dtstart=parse_datetime("1997-09-02T09:00:00Z"),
        dtend=parse_datetime("1997-09-02T10:00:00Z"),
        recurrence_rule=recurrence_rule,
    )
    url = reverse(
        "plugins-api:nautobot_schedule-api:event-recurrences",
        kwargs={"pk": event.id},
    )
    response = api_client_with_credentials.get(
        url,
        data={
            "start": "1997-09-02T09:00:00Z",
            "end": "1997-09-04T9:00:00Z",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        "1997-09-02T09:00:00Z",
        "1997-09-03T09:00:00Z",
        "1997-09-04T09:00:00Z",
    ]
