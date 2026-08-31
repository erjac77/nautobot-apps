import re
from datetime import datetime, timedelta
from typing import Any, ClassVar

from dateutil import rrule
from django.conf import settings as django_settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.translation import gettext_lazy as _
from nautobot.apps.models import extras_features
from nautobot.core.models.generics import PrimaryModel

from nautobot_calendars.constants import FIRST_WEEK_DAY
from nautobot_calendars.validators import JSONSchemaValidator


def make_aware(dt: datetime) -> datetime:
    if timezone.is_aware(dt):
        return dt
    return timezone.make_aware(dt)


@extras_features("custom_links", "custom_validators", "export_templates", "graphql", "webhooks")
class CalendarType(PrimaryModel, models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"{self.name}"


@extras_features("custom_links", "custom_validators", "export_templates", "graphql", "webhooks")
class Calendar(PrimaryModel, models.Model):
    calendar_type = models.ForeignKey(
        CalendarType, on_delete=models.CASCADE, related_name="calendars"
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"{self.name}"


@extras_features("graphql")
class RecurrenceRule(PrimaryModel, models.Model):
    """Provides a grouping of properties that describe a recurrence rule.

    See: https://datatracker.ietf.org/doc/html/rfc5545#section-3.3.10
    """

    class FrequencyChoices(models.IntegerChoices):
        SECONDLY = rrule.SECONDLY, _("SECONDLY")
        MINUTELY = rrule.MINUTELY, _("MINUTELY")
        HOURLY = rrule.HOURLY, _("HOURLY")
        DAILY = rrule.DAILY, _("DAILY")
        WEEKLY = rrule.WEEKLY, _("WEEKLY")
        MONTHLY = rrule.MONTHLY, _("MONTHLY")
        YEARLY = rrule.YEARLY, _("YEARLY")

    class WeekdayChoices(models.IntegerChoices):
        MO = rrule.MO.weekday, _("MO (Monday)")
        TU = rrule.TU.weekday, _("TU (Tuesday)")
        WE = rrule.WE.weekday, _("WE (Wednesday)")
        TH = rrule.TH.weekday, _("TH (Thursday)")
        FR = rrule.FR.weekday, _("FR (Friday)")
        SA = rrule.SA.weekday, _("SA (Saturday)")
        SU = rrule.SU.weekday, _("SU (Sunday)")

    _byparams: ClassVar[dict[str, Any]] = {
        "bysecond": {
            "schema": {
                "type": "array",
                "items": {"type": "integer", "minimum": 0, "maximum": 60},
            },
        },
        "byminute": {
            "schema": {
                "type": "array",
                "items": {"type": "integer", "minimum": 0, "maximum": 59},
            },
        },
        "byhour": {
            "schema": {
                "type": "array",
                "items": {"type": "integer", "minimum": 0, "maximum": 23},
            },
        },
        "byday": {
            "schema": {
                "type": "array",
                "items": {
                    "type": "string",
                    "pattern": "^([+-]?[0-4]?[0-9]|5[0-3])?(MO|TU|WE|TH|FR|SA|SU)$",
                },
            },
        },
        "bymonthday": {
            "schema": {
                "type": "array",
                "items": {
                    "anyOf": [
                        {"type": "integer", "minimum": -31, "maximum": -1},
                        {"type": "integer", "minimum": 1, "maximum": 31},
                    ],
                },
            },
        },
        "byyearday": {
            "schema": {
                "type": "array",
                "items": {
                    "anyOf": [
                        {"type": "integer", "minimum": -366, "maximum": -1},
                        {"type": "integer", "minimum": 1, "maximum": 366},
                    ],
                },
            },
        },
        "byweekno": {
            "schema": {
                "type": "array",
                "items": {
                    "anyOf": [
                        {"type": "integer", "minimum": -53, "maximum": -1},
                        {"type": "integer", "minimum": 1, "maximum": 53},
                    ],
                },
            },
        },
        "bymonth": {
            "schema": {
                "type": "array",
                "items": {"type": "integer", "minimum": 1, "maximum": 12},
            },
        },
        "bysetpos": {
            "schema": {
                "type": "array",
                "items": {
                    "anyOf": [
                        {"type": "integer", "minimum": -366, "maximum": -1},
                        {"type": "integer", "minimum": 1, "maximum": 366},
                    ],
                },
            },
        },
    }

    name = models.CharField(max_length=255)
    freq = models.PositiveIntegerField(
        choices=FrequencyChoices.choices,
        help_text="The frequency with which the event should be repeated. Valid values are SECONDLY, MINUTELY, HOURLY, DAILY, WEEKLY, MONTHLY and YEARLY.",  # noqa: E501
    )
    interval = models.PositiveIntegerField(
        default=1,
        help_text="A positive integer representing at which intervals the recurrence rule repeats. The default value is '1'.",  # noqa: E501
    )
    count = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="The number of occurrences at which to range-bound the recurrence.",
    )
    until = models.DateTimeField(
        blank=True,
        null=True,
        help_text="The DATE-TIME value that bounds the recurrence rule in an inclusive manner.",
    )
    bysecond = models.JSONField(
        blank=True,
        default=tuple,
        help_text="A COMMA-separated list of seconds within a minute. Valid values are 0 to 60.",
        validators=[JSONSchemaValidator(schema=_byparams["bysecond"]["schema"])],  # ty:ignore[invalid-argument-type]
    )
    byminute = models.JSONField(
        blank=True,
        default=list,
        help_text="A COMMA-separated list of minutes within an hour. Valid values are 0 to 59.",
        validators=[JSONSchemaValidator(schema=_byparams["byminute"]["schema"])],  # ty:ignore[invalid-argument-type]
    )
    byhour = models.JSONField(
        blank=True,
        default=list,
        help_text="A COMMA-separated list of hours of the day. Valid values are 0 to 23.",
        validators=[JSONSchemaValidator(schema=_byparams["byhour"]["schema"])],  # ty:ignore[invalid-argument-type]
    )
    byday = models.JSONField(
        blank=True,
        default=list,
        help_text="A COMMA-separated list of days of the week. Valid values are SU, MO, TU, WE, TH, FR and SA. Each BYDAY value can also be preceded by a positive (+n) or negative (-n) integer indicating the nth occurrence of a specific day within the MONTHLY or YEARLY 'RRULE'.",  # noqa: E501
        validators=[JSONSchemaValidator(schema=_byparams["byday"]["schema"])],  # ty:ignore[invalid-argument-type]
    )
    bymonthday = models.JSONField(
        blank=True,
        default=list,
        help_text="COMMA-separated list of days of the month. Valid values are 1 to 31 or -31 to -1.",  # noqa: E501
        validators=[JSONSchemaValidator(schema=_byparams["bymonthday"]["schema"])],  # ty:ignore[invalid-argument-type]
    )
    byyearday = models.JSONField(
        blank=True,
        default=list,
        help_text="A COMMA-separated list of days of the year. Valid values are 1 to 366 or -366 to -1.",  # noqa: E501
        validators=[JSONSchemaValidator(schema=_byparams["byyearday"]["schema"])],  # ty:ignore[invalid-argument-type]
    )
    byweekno = models.JSONField(
        blank=True,
        default=list,
        help_text="A COMMA-separated list of ordinals specifying weeks of the year. Valid values are 1 to 53 or -53 to -1.",  # noqa: E501
        validators=[JSONSchemaValidator(schema=_byparams["byweekno"]["schema"])],  # ty:ignore[invalid-argument-type]
    )
    bymonth = models.JSONField(
        blank=True,
        default=list,
        help_text="A COMMA-separated list of months of the year. Valid values are 1 to 12.",
        validators=[JSONSchemaValidator(schema=_byparams["bymonth"]["schema"])],  # ty:ignore[invalid-argument-type]
    )
    bysetpos = models.JSONField(
        blank=True,
        default=list,
        help_text="A COMMA-separated list of values that corresponds to the nth occurrence within the set of recurrence instances specified by the rule.",  # noqa: E501
        validators=[JSONSchemaValidator(schema=_byparams["bysetpos"]["schema"])],  # ty:ignore[invalid-argument-type]
    )
    wkst = models.PositiveIntegerField(
        choices=WeekdayChoices.choices,
        default=FIRST_WEEK_DAY,
        help_text="The day on which the workweek starts. Valid values are MO, TU, WE, TH, FR, SA, and SU.",  # noqa: E501
    )

    def __str__(self) -> str:
        return f"{self.name}"

    def _to_dateutil_rrule_weekday(self, day: str) -> rrule.weekday:
        day_map = {
            "MO": rrule.MO,
            "TU": rrule.TU,
            "WE": rrule.WE,
            "TH": rrule.TH,
            "FR": rrule.FR,
            "SA": rrule.SA,
            "SU": rrule.SU,
        }
        day_pattern = re.compile(self._byparams["byday"]["schema"]["items"]["pattern"])

        result = day_map["MO"]
        day_matches = day_pattern.match(day.strip())
        if day_matches:
            offset, weekday = day_matches.groups()
            result = day_map[weekday]
            if offset:
                result = result(int(offset))

        return result

    def to_dateutil_rrule(self, dtstart: datetime | None = None) -> rrule.rrule:
        rrule_kwargs = {}

        for byparam_key in self._byparams:
            _byparam_value = []
            byparam_value = getattr(self, byparam_key, [])

            if byparam_value:
                # Dateutil renamed BYDAY to avoid the ambiguity
                # https://dateutil.readthedocs.io/en/stable/rrule.html#classes
                if byparam_key == "byday":
                    byparam_key = "byweekday"  # noqa: PLW2901
                    _byparam_value = [
                        self._to_dateutil_rrule_weekday(byparam_value[i])
                        for i in range(len(byparam_value))
                    ]
                else:
                    _byparam_value = byparam_value

                if _byparam_value:
                    rrule_kwargs.update({byparam_key: _byparam_value})

        return rrule.rrule(
            freq=self.freq,
            dtstart=dtstart,
            interval=self.interval,
            wkst=self.wkst,
            count=self.count,
            until=self.until,
            **rrule_kwargs,
        )

    def clean(self) -> None:
        try:
            self.to_dateutil_rrule()
        except (TypeError, ValueError) as err:
            raise ValidationError(str(err)) from err


@extras_features("custom_links", "custom_validators", "export_templates", "graphql", "webhooks")
class Event(PrimaryModel, models.Model):
    class PriorityChoices(models.IntegerChoices):
        LOW = 0, _("Low")
        NORMAL = 1, _("Normal")
        HIGH = 2, _("High")

    date_schema: ClassVar[dict[str, Any]] = {
        "type": "array",
        "items": {
            "pattern": "^\\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\\d|3[01]) ([01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d$",  # noqa: E501
        },
    }

    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name="events")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    dtstart = models.DateTimeField(verbose_name="Start")
    dtend = models.DateTimeField(verbose_name="End")
    organizer = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="events",
    )
    priority = models.PositiveIntegerField(
        choices=PriorityChoices.choices, default=PriorityChoices.NORMAL
    )
    # A rule for recurring events.
    recurrence_rule = models.ForeignKey(
        RecurrenceRule, blank=True, null=True, on_delete=models.SET_NULL, related_name="events"
    )
    # A list of datetime exceptions for recurring events.
    exdates = models.JSONField(
        blank=True,
        default=list,
        help_text="Additional date-times to exclude from the event. Format: 'YYYY-MM-DD HH:MM:SS'.",
        validators=[JSONSchemaValidator(schema=date_schema)],  # ty:ignore[invalid-argument-type]
    )
    # A list of datetime values for recurring events.
    rdates = models.JSONField(
        blank=True,
        default=list,
        help_text="Additional date-times to include in the event. Format: 'YYYY-MM-DD HH:MM:SS'.",
        validators=[JSONSchemaValidator(schema=date_schema)],  # ty:ignore[invalid-argument-type]
    )

    def __str__(self) -> str:
        return f"{self.title}"

    @property
    def duration(self) -> timedelta:
        return self.dtend - self.dtstart

    def _rruleset(self) -> rrule.rruleset:
        rr = self.recurrence_rule
        rset = rrule.rruleset()
        if isinstance(rr, RecurrenceRule):
            rset.rrule(rr.to_dateutil_rrule(self.dtstart))
            if self.exdates:
                for exd in self.exdates:
                    rset.exdate(make_aware(parse_datetime(exd)))  # ty:ignore[invalid-argument-type]
            if self.rdates:
                for rd in self.rdates:
                    rset.rdate(make_aware(parse_datetime(rd)))  # ty:ignore[invalid-argument-type]
        return rset

    def recurrences(
        self,
        after: datetime | None = None,
        before: datetime | None = None,
        inc: bool = True,  # noqa: FBT001, FBT002
    ) -> list[datetime]:
        """Returns all the occurrences of the event between after and before.

        Args:
            after (datetime): The datetime at which to start generating recurrences.
            before (datetime): The datetime at which to end generating recurrences.
            inc (bool): If dt is an instance of the rule and inc is True,
                it is included in the output.

        Returns: The recurrences.
        """
        if after and before:
            if self.recurrence_rule:
                return self._rruleset().between(after, before, inc)
            if (inc and self.dtstart >= after and self.dtstart <= before) or (
                not inc and self.dtstart > after and self.dtstart < before
            ):
                return [self.dtstart]
        return []

    def intersect(self, dtstart: datetime | None = None, dtend: datetime | None = None) -> bool:
        """Returns true if overlap (intersect) within two provided dt is found.

        Args:
            dtstart (datetime): The datetime at which to start the search.
            dtend (datetime): The datetime at which to end the search.

        Returns: True if overlap, else False.
        """
        if dtstart and dtend:
            recurrences = self.recurrences(
                dtstart - self.duration,
                dtend + self.duration,
            )
            for rec in recurrences:
                latest_start = max(dtstart, rec)
                earliest_end = min(dtend, rec + self.duration)
                if latest_start <= earliest_end:
                    return True
        return False
