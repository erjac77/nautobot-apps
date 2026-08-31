"""Shared fixtures for Nautobot unit tests."""

import pytest
from nautobot.users.factory import UserFactory
from pytest_factoryboy import register
from rest_framework.test import APIClient


register(UserFactory)


@pytest.fixture
def api_client_with_credentials(user_factory: UserFactory) -> APIClient:
    user = user_factory.build(is_active=True, is_superuser=True)
    client = APIClient()
    client.force_authenticate(user=user)
    return client
