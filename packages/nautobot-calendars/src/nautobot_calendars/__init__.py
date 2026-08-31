from importlib import metadata
from typing import Any

from nautobot.apps import NautobotAppConfig
from nautobot.core.signals import nautobot_database_ready


app_name = "nautobot_calendars"
app_version = metadata.version(app_name)


class NautobotCalendarsAppConfig(NautobotAppConfig):
    author = "Eric Jacob"
    author_email = "erjac77@gmail.com"
    base_url = "calendars"
    description = "Nautobot App to define and assign maintenance or blackout schedules to an object (ex: Device)."  # noqa: E501
    min_version = "3.1.0"
    name = app_name
    verbose_name = "Nautobot Calendars App"
    version = app_version

    default_settings: dict[str, Any] = {
        "first_week_day": 0,
        "initial_view": "dayGridMonth",
    }

    def ready(self) -> None:
        from .signals import (  # noqa: PLC0415
            post_migrate_create_calendar_types,
            post_migrate_create_relationships,
        )

        nautobot_database_ready.connect(post_migrate_create_calendar_types, sender=self)
        nautobot_database_ready.connect(post_migrate_create_relationships, sender=self)

        super().ready()


config = NautobotCalendarsAppConfig
