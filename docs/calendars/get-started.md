---
icon: lucide/rocket
---

# Get started

## Prerequisites

The app is compatible with:

- Nautobot 3.1.0 and higher.
- PostgreSQL and MySQL databases.

## Installation

!!! note

    Apps can be installed from the [Python Package Index](https://pypi.org), from the project Git repository or locally. See the [Nautobot documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/administration/installation/app-install/) for more details. The pip package name for this app is `nautobot-calendars`.

To install the app via PyPI:

```shell
pip install nautobot-calendars
```

To install from the project Git repository:

```shell
pip install "nautobot-calendars @ git+https://github.com/erjac77/nautobot-apps@main#subdirectory=packages/nautobot-calendars"
```

Once installed, the app needs to be enabled in your Nautobot configuration:

- Append "`nautobot_calendars`" to the `PLUGINS` list.
- Append the "`nautobot_calendars`" dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.

The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

```python
# In your nautobot_config.py
PLUGINS = ["nautobot_calendars"]

# PLUGINS_CONFIG = {
#   "nautobot_calendars": {
#     "first_week_day": 0,
#     "initial_view": "dayGridMonth",
#   }
# }
```

## Configuration

Integration behavior can be controlled with the following settings:

| Variable         | Type    | Description                                                                                                                                     |
| ---------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `first_week_day` | integer | The first day of the week. `0` for Monday or `6` for Sunday. Default: `0`.                                                                      |
| `initial_view`   | string  | The initial view when the calendar loads. Available views: `dayGridYear`, `dayGridMonth`, `dayGridWeek`, `dayGridDay`. Default: `dayGridMonth`. |
