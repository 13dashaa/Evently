import pytest
from django.urls import reverse
from rest_framework import status

from events.models import Venue


@pytest.mark.django_db
def test_create_venue_success(api_client, venue_data: dict) -> None:
    url = reverse("venue-list")
    response = api_client.post(url, data=venue_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Venue.objects.count() == 1
    assert Venue.objects.get().name == venue_data["name"]


@pytest.mark.django_db
def test_create_venue_failure_invalid_data(api_client, venue_data: dict) -> None:
    url = reverse("venue-list")
    venue_data["capacity"] = -100
    response = api_client.post(url, data=venue_data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Venue.objects.count() == 0


@pytest.mark.django_db
def test_list_venue_success(api_client, create_venue) -> None:
    create_venue(name="Venue1")
    create_venue(name="Venue2")
    url = reverse("venue-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_retrieve_venue_success(api_client, create_venue) -> None:
    venue = create_venue(name="Venue1")
    url = reverse("venue-detail", args=[venue.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert Venue.objects.get().name == "Venue1"


@pytest.mark.django_db
def test_retrieve_venue_failure_not_found(api_client, create_venue) -> None:
    create_venue(name="Venue1")
    url = reverse("venue-detail", args=[999999])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_venue_success(api_client, create_venue, venue_data):
    venue = create_venue(name="Old Name")
    url = reverse("venue-detail", args=[venue.id])
    data = {"name": venue_data["name"]}
    response = api_client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    venue.refresh_from_db()
    assert venue.name == data["name"]


@pytest.mark.django_db
def test_update_venue_failure_invalid_data(api_client, create_venue, venue_data):
    venue = create_venue(name="Old Name")
    url = reverse("venue-detail", args=[venue.id])
    data = {"capacity": "not an integer"}
    response = api_client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    venue.refresh_from_db()
    assert venue.capacity != "not an integer"


@pytest.mark.django_db
def test_delete_venue_success(api_client, create_venue) -> None:
    venue = create_venue(name="Venue1")
    url = reverse("venue-detail", args=[venue.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Venue.objects.count() == 0


@pytest.mark.django_db
def test_delete_venue_failure_not_found(api_client, create_venue) -> None:
    create_venue(name="Venue1")
    url = reverse("venue-detail", args=[999])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
