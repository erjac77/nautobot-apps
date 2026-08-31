"""Pytest plugin for Nautobot."""

import pytest
from nautobot import setup


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests() -> None:
    """Hook for using nautobot-server.

    Import settings FIRST before pytest-django.
    """
    setup()
