from typing import cast

from nautobot.apps.config import get_app_settings_or_config


FIRST_WEEK_DAY: int = cast("int", get_app_settings_or_config("nautobot_schedule", "first_week_day"))
if FIRST_WEEK_DAY not in (0, 6):
    FIRST_WEEK_DAY = 0

BLACKOUT_SCHEDULE: str = "Blackout"
MAINTENANCE_SCHEDULE: str = "Maintenance"
