import pytest
from django.urls import reverse
from rest_framework import status

from events.models import Venue


@pytest.mark.django_db
def test_create_venue(api_client, venue_data: dict) -> None:
    url = reverse("venue-list")
    response = api_client.post(url, data=venue_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Venue.objects.count() == 1
    assert Venue.objects.get().name == venue_data["name"]
