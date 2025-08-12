import pytest
from rest_framework.test import APIClient

from events.models import Venue


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def venue_data() -> dict:
    return {
        "name": "The Grand Theatre",
        "address": "123 Main Street, City",
        "capacity": 1500,
    }


@pytest.fixture
def create_venue():
    def _create_venue(**kwargs):
        return Venue.objects.create(
            name=kwargs.get("name", "Test Venue"),
            address=kwargs.get("address", "Test Address"),
            capacity=kwargs.get("capacity", 100),
        )

    return _create_venue
