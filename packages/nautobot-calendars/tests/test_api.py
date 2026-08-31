import pytest
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from nautobot_calendars.factories import EventFactory, RecurrenceRuleFactory
from nautobot_calendars.models import RecurrenceRule
from rest_framework import status
from rest_framework.test import APIClient


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
        "plugins-api:nautobot_calendars-api:event-recurrences",
        kwargs={"pk": event.id},
    )
    response = api_client_with_credentials.get(
        url,
        data={
            "after": "1997-09-02T09:00:00Z",
            "before": "1997-09-04T9:00:00Z",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        "1997-09-02T09:00:00Z",
        "1997-09-03T09:00:00Z",
        "1997-09-04T09:00:00Z",
    ]
