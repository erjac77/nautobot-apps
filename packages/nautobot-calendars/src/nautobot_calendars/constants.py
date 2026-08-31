from typing import Any

from django.conf import settings


PLUGIN_CFG: dict[str, Any] = settings.PLUGINS_CONFIG.get("nautobot_calendars", {})

FIRST_WEEK_DAY: int = PLUGIN_CFG.get("first_week_day", 0)
if FIRST_WEEK_DAY not in (0, 6):
    FIRST_WEEK_DAY = 0

BLACKOUT_CALENDAR: str = "Blackout"
MAINTENANCE_CALENDAR: str = "Maintenance"
