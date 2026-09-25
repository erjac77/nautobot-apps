"""Nautobot command-line utility for administrative tasks."""

from io import StringIO

from dotenv import load_dotenv
from nautobot.core.cli import main


if __name__ == "__main__":
    config = StringIO("NAUTOBOT_CONFIG=src/nautobot_apps/nautobot_config_dev.py")
    load_dotenv(stream=config)
    load_dotenv("nautobot.env")
    main()
