import pytest
from rest_framework.test import APIClient


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
