import pytest
from django.urls import reverse
from rest_framework import status

from events.models import Event


@pytest.mark.django_db
def test_create_event_success_authenticated(api_client, create_user, event_data: dict):
    user = create_user("organizer")
    api_client.force_authenticate(user=user)
    url = reverse("event-list")
    response = api_client.post(url, data=event_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Event.objects.count() == 1
    assert Event.objects.get().organizer == user
    assert Event.objects.get().name == event_data["name"]


@pytest.mark.django_db
def test_create_event_failure_unauthenticated(api_client, event_data: dict):

    url = reverse("event-list")
    response = api_client.post(url, data=event_data, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Event.objects.count() == 0


@pytest.mark.django_db
def test_create_event_failure_invalid_data(api_client, create_user, event_data: dict):
    user = create_user("organizer")
    api_client.force_authenticate(user=user)
    invalid_data = event_data.copy()
    invalid_data["name"] = ""
    url = reverse("event-list")
    response = api_client.post(url, data=invalid_data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Event.objects.count() == 0


@pytest.mark.django_db
def test_list_event_success(api_client, create_event) -> None:
    create_event(name="Event1")
    create_event(name="Event2")
    url = reverse("event-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_retrieve_event_success(api_client, create_event) -> None:
    test_event = create_event(name="Test event")
    url = reverse("event-detail", args=[test_event.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == test_event.name


@pytest.mark.django_db
def test_retrieve_failure_not_found(api_client, create_event) -> None:
    create_event(name="Test event")
    url = reverse("event-detail", args=[9999])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_event_success_organizer(api_client, create_event, create_user):
    organizer = create_user("organizer")
    event = create_event(organizer=organizer, name="Old name")
    api_client.force_authenticate(user=organizer)

    url = reverse("event-detail", args=[event.id])
    data = {"name": "New name"}
    response = api_client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    event.refresh_from_db()
    assert event.name == "New name"


@pytest.mark.django_db
def test_update_event_failure_not_organizer(api_client, create_event, create_user):
    organizer = create_user("organizer")
    other_user = create_user("other_user")

    event = create_event(organizer=organizer, name="Old name")
    api_client.force_authenticate(user=other_user)

    url = reverse("event-detail", args=[event.id])
    data = {"name": "New name"}
    response = api_client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    event.refresh_from_db()
    assert event.name != "New name"


@pytest.mark.django_db
def test_delete_event_success_organizer(api_client, create_event, create_user):
    organizer = create_user("organizer")
    event = create_event(organizer=organizer, name="To delete")
    api_client.force_authenticate(user=organizer)

    url = reverse("event-detail", args=[event.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Event.objects.count() == 0


@pytest.mark.django_db
def test_delete_event_failure_not_organizer(api_client, create_event, create_user):
    organizer = create_user("organizer")
    other_user = create_user("other_user")

    event = create_event(organizer=organizer, name="To delete")
    api_client.force_authenticate(user=other_user)

    url = reverse("event-detail", args=[event.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Event.objects.count() == 1
