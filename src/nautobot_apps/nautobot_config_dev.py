"""Nautobot configuration file for development."""

import os
from typing import Any, LiteralString

from nautobot.core.settings import *
from nautobot.core.settings_funcs import is_truthy


BANNER_TOP: str | LiteralString = os.getenv("NAUTOBOT_BANNER_TOP", "Local")

# Debugging defaults to True rather than False for the development environment.
DEBUG: bool = is_truthy(os.getenv("NAUTOBOT_DEBUG", "True"))

# Django Debug Toolbar - enabled only when debugging.
if DEBUG:
    if "debug_toolbar" not in INSTALLED_APPS:
        INSTALLED_APPS.append("debug_toolbar")
    if "debug_toolbar.middleware.DebugToolbarMiddleware" not in MIDDLEWARE:
        MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    # By default the toolbar only displays when the request is coming from one of
    # INTERNAL_IPS. For the Docker dev environment, we don't know in advance what
    # that IP may be, so override to skip that check.
    DEBUG_TOOLBAR_CONFIG: dict[str, Any] = {
        "SHOW_TOOLBAR_CALLBACK": lambda _request: DEBUG,
    }


PLUGINS: list[str] = ["nautobot_calendars"]
