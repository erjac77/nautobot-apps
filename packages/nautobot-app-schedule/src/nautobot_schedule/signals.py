import logging
from typing import Any

from django.apps import AppConfig
from django.apps import apps as global_apps
from django.apps.registry import Apps
from nautobot.extras.choices import RelationshipTypeChoices

from nautobot_schedule.constants import BLACKOUT_SCHEDULE, MAINTENANCE_SCHEDULE


logger = logging.getLogger(__name__)


def post_migrate_create_schedule_types(
    sender: AppConfig,
    apps: Apps = global_apps,  # noqa: ARG001
    **kwargs: dict[str, Any],  # noqa: ARG001
) -> None:
    logger.info("Creating blackout and maintenance schedule types...")

    ScheduleType = sender.get_model("ScheduleType")

    for schedule_type_dict in [
        {
            "name": BLACKOUT_SCHEDULE,
            "description": "Blackout windows specify times during which normal change activity should not be scheduled.",  # noqa: E501
        },
        {
            "name": MAINTENANCE_SCHEDULE,
            "description": "Maintenance windows specify times during which change requests should be scheduled.",  # noqa: E501
        },
    ]:
        ScheduleType.objects.get_or_create(
            name=schedule_type_dict["name"],
            defaults={"description": schedule_type_dict["description"]},
        )


def post_migrate_create_relationships(
    sender: AppConfig,
    apps: Apps = global_apps,
    **kwargs: dict[str, Any],  # noqa: ARG001
) -> None:
    logger.info("Creating relationship between devices and maintenance schedule...")

    Schedule = sender.get_model("Schedule")
    ContentType = apps.get_model("contenttypes", "ContentType")
    Device = apps.get_model("dcim", "Device")
    Relationship = apps.get_model("extras", "Relationship")

    for relationship_dict in [
        {
            "label": "Assign maintenance schedule to device",
            "key": "assign_maintenance_schedule_to_device",
            "type": RelationshipTypeChoices.TYPE_MANY_TO_MANY,
            "source_type": ContentType.objects.get_for_model(Schedule),
            "source_label": "Applies to",
            "source_filter": {"schedule_type": [MAINTENANCE_SCHEDULE]},
            "destination_type": ContentType.objects.get_for_model(Device),
            "destination_label": "Maintenance schedule",
        },
    ]:
        Relationship.objects.get_or_create(
            label=relationship_dict["label"], defaults=relationship_dict
        )
