import logging
from typing import Any

from django.apps import AppConfig
from django.apps import apps as global_apps
from django.apps.registry import Apps
from nautobot.extras.choices import RelationshipTypeChoices

from nautobot_calendars.constants import BLACKOUT_CALENDAR, MAINTENANCE_CALENDAR


logger = logging.getLogger(__name__)


def post_migrate_create_calendar_types(
    sender: AppConfig,
    apps: Apps = global_apps,  # noqa: ARG001
    **kwargs: dict[str, Any],  # noqa: ARG001
) -> None:
    logger.info("Creating blackout and maintenance calendar types...")

    CalendarType = sender.get_model("CalendarType")

    for calendar_type_dict in [
        {
            "name": BLACKOUT_CALENDAR,
            "description": "Blackout windows specify times during which normal change activity should not be scheduled.",  # noqa: E501
        },
        {
            "name": MAINTENANCE_CALENDAR,
            "description": "Maintenance windows specify times during which change requests should be scheduled.",  # noqa: E501
        },
    ]:
        CalendarType.objects.get_or_create(
            name=calendar_type_dict["name"],
            defaults={"description": calendar_type_dict["description"]},
        )


def post_migrate_create_relationships(
    sender: AppConfig,
    apps: Apps = global_apps,
    **kwargs: dict[str, Any],  # noqa: ARG001
) -> None:
    logger.info("Creating relationship between devices and maintenance calendars...")

    Calendar = sender.get_model("Calendar")
    ContentType = apps.get_model("contenttypes", "ContentType")
    Device = apps.get_model("dcim", "Device")
    Relationship = apps.get_model("extras", "Relationship")

    for relationship_dict in [
        {
            "label": "Assign maintenance schedule to device",
            "key": "assign_maintenance_schedule_to_device",
            "type": RelationshipTypeChoices.TYPE_MANY_TO_MANY,
            "source_type": ContentType.objects.get_for_model(Calendar),
            "source_label": "Applies to",
            "source_filter": {"calendar_type": [MAINTENANCE_CALENDAR]},
            "destination_type": ContentType.objects.get_for_model(Device),
            "destination_label": "Maintenance schedule",
        },
    ]:
        Relationship.objects.get_or_create(
            label=relationship_dict["label"], defaults=relationship_dict
        )
