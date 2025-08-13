import pytest
from django.urls import reverse
from rest_framework import status

from events.models import Venue
from orders.models import Ticket, TicketType


@pytest.mark.django_db
def test_create_ticket_by_organizer_success(
    api_client, create_user, create_event, ticket_data: dict
) -> None:
    organizer = create_user("organizer")
    event = create_event(organizer=organizer)
    api_client.force_authenticate(user=organizer)
    url = reverse("ticket-list")
    data = ticket_data.copy()
    data["event"] = event.id
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Ticket.objects.count() == 1
    assert Ticket.objects.get().event == event


@pytest.mark.django_db
def test_create_ticket_by_admin_success(
    api_client, create_user, create_event, ticket_data: dict
) -> None:
    admin = create_user("admin", is_staff=True)
    event = create_event()
    api_client.force_authenticate(user=admin)
    url = reverse("ticket-list")
    data = ticket_data.copy()
    data["event"] = event.id
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Ticket.objects.count() == 1


@pytest.mark.django_db
def test_create_ticket_by_non_organizer_failure(
    api_client, create_user, create_event, ticket_data: dict
) -> None:
    organizer = create_user("organizer")
    non_organizer = create_user("non_organizer")
    event = create_event(organizer=organizer)
    api_client.force_authenticate(user=non_organizer)
    url = reverse("ticket-list")
    data = ticket_data.copy()
    data["event"] = event.id
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Ticket.objects.count() == 0


@pytest.mark.django_db
def test_create_ticket_by_unauthenticated_user_failure(
    api_client, create_event, ticket_data: dict
) -> None:
    event = create_event()
    url = reverse("ticket-list")
    data = ticket_data.copy()
    data["event"] = event.id
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Ticket.objects.count() == 0


@pytest.mark.django_db
def test_list_ticket_success(api_client, create_ticket) -> None:
    create_ticket(type=TicketType.vip)
    create_ticket(type=TicketType.standard)
    url = reverse("ticket-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_retrieve_ticket_success(api_client, create_ticket) -> None:
    ticket = create_ticket()
    url = reverse("ticket-detail", args=[ticket.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == ticket.id


@pytest.mark.django_db
def test_retrieve_ticket_failure_not_found(api_client, create_ticket) -> None:
    create_ticket()
    url = reverse("ticket-detail", args=[999999])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_ticket_by_organizer_success(
    api_client, create_ticket, create_event, create_user
):
    organizer = create_user("organizer")
    event = create_event(organizer=organizer)
    api_client.force_authenticate(user=organizer)
    ticket = create_ticket(event=event)
    url = reverse("ticket-detail", args=[ticket.id])
    data = {"price": 500.00}
    response = api_client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    ticket.refresh_from_db()
    assert ticket.price == 500


@pytest.mark.django_db
def test_update_ticket_by_non_organizer_failure(
    api_client, create_user, create_event, create_ticket
):
    organizer = create_user("organizer")
    non_organizer = create_user("non_organizer")
    event = create_event(organizer=organizer)
    ticket = create_ticket(event=event)
    api_client.force_authenticate(user=non_organizer)

    url = reverse("ticket-detail", args=[ticket.id])
    data = {"price": 500.00}
    response = api_client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    ticket.refresh_from_db()
    assert ticket.price != 500.00


@pytest.mark.django_db
def test_update_ticket_by_admin_success(
    api_client, create_ticket, create_event, create_user
):
    organizer = create_user("organizer")
    admin = create_user("admin", is_staff=True)
    event = create_event(organizer=organizer)
    api_client.force_authenticate(user=admin)
    ticket = create_ticket(event=event)
    url = reverse("ticket-detail", args=[ticket.id])
    data = {"price": 500.00}
    response = api_client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    ticket.refresh_from_db()
    assert ticket.price == 500


@pytest.mark.django_db
def test_update_ticket_failure_invalid_data(
    api_client, create_user, create_event, create_ticket
):
    organizer = create_user("organizer")
    event = create_event(organizer=organizer)
    ticket = create_ticket(event=event, type=TicketType.vip)
    api_client.force_authenticate(user=organizer)
    url = reverse("ticket-detail", args=[ticket.id])
    data = {"quantity": 4.5}
    response = api_client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    ticket.refresh_from_db()
    assert ticket.type != TicketType.standard


@pytest.mark.django_db
def test_delete_ticket_by_organizer_success(
    api_client, create_ticket, create_event, create_user
):
    organizer = create_user("organizer")
    event = create_event(organizer=organizer)
    api_client.force_authenticate(user=organizer)
    ticket = create_ticket(event=event)
    url = reverse("ticket-detail", args=[ticket.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Ticket.objects.count() == 0


@pytest.mark.django_db
def test_delete_ticket_by_admin_success(
    api_client, create_ticket, create_event, create_user
):
    organizer = create_user("organizer")
    admin = create_user("admin", is_staff=True)
    event = create_event(organizer=organizer)
    api_client.force_authenticate(user=admin)
    ticket = create_ticket(event=event)
    url = reverse("ticket-detail", args=[ticket.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Ticket.objects.count() == 0


@pytest.mark.django_db
def test_delete_ticket_failure_not_found(
    api_client, create_ticket, create_event, create_user
) -> None:
    organizer = create_user("organizer")
    event = create_event(organizer=organizer)
    create_ticket(event=event)
    api_client.force_authenticate(user=organizer)
    url = reverse("ticket-detail", args=[999])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_ticket_by_non_organizer_failure(
    api_client, create_user, create_event, create_ticket
):
    organizer = create_user("organizer")
    non_organizer = create_user("non_organizer")
    event = create_event(organizer=organizer)
    ticket = create_ticket(event=event)
    api_client.force_authenticate(user=non_organizer)

    url = reverse("ticket-detail", args=[ticket.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Ticket.objects.count() == 1
