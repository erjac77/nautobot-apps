from importlib import metadata
from typing import Any

from nautobot.apps import NautobotAppConfig
from nautobot.core.signals import nautobot_database_ready


app_name = "nautobot_schedule"
app_version = metadata.version(app_name)


class NautobotScheduleAppConfig(NautobotAppConfig):
    author = "Eric Jacob"
    author_email = "erjac77@gmail.com"
    base_url = "schedule"
    description = "Nautobot App to define and assign maintenance or blackout schedules to an object (ex: Device)."  # noqa: E501
    docs_view_name = "plugins:nautobot_schedule:docs"
    min_version = "3.1.0"
    name = app_name
    searchable_models = ["schedule", "events"]
    verbose_name = "Nautobot Schedule App"
    version = app_version

    default_settings: dict[str, Any] = {
        "first_week_day": 0,
        "initial_view": "dayGridMonth",
    }

    required_settings = []

    def ready(self) -> None:
        from .signals import (  # noqa: PLC0415
            post_migrate_create_relationships,
            post_migrate_create_schedule_types,
        )

        nautobot_database_ready.connect(post_migrate_create_schedule_types, sender=self)
        nautobot_database_ready.connect(post_migrate_create_relationships, sender=self)

        super().ready()


config = NautobotScheduleAppConfig
