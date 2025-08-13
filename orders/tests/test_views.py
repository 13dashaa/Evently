import pytest
from django.urls import reverse
from rest_framework import status

from orders.models import Ticket, TicketType


@pytest.mark.django_db
@pytest.mark.parametrize(
    "user_type, expected_status",
    [
        ("organizer", status.HTTP_201_CREATED),
        ("admin", status.HTTP_201_CREATED),
        ("non_organizer", status.HTTP_403_FORBIDDEN),
        ("unauthenticated", status.HTTP_403_FORBIDDEN),
    ],
)
def test_create_ticket_permissions(
    api_client, create_user, create_event, ticket_data: dict, user_type, expected_status
) -> None:
    organizer = create_user("organizer")
    event = create_event(organizer=organizer)

    if user_type == "organizer":
        current_user = organizer
    elif user_type == "admin":
        current_user = create_user("admin", is_staff=True)
    elif user_type == "non_organizer":
        current_user = create_user("non_organizer")
    else:
        current_user = None

    if current_user:
        api_client.force_authenticate(user=current_user)

    url = reverse("ticket-list")
    data = ticket_data.copy()
    data["event"] = event.id
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == expected_status
    if expected_status == status.HTTP_201_CREATED:
        assert Ticket.objects.count() == 1
    else:
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
@pytest.mark.parametrize(
    "method, user_type, data, expected_status",
    [
        ("patch", "organizer", {"price": 500.00}, status.HTTP_200_OK),
        ("patch", "admin", {"price": 500.00}, status.HTTP_200_OK),
        ("patch", "non_organizer", {"price": 500.00}, status.HTTP_403_FORBIDDEN),
        ("patch", "organizer", {"quantity": 5.5}, status.HTTP_400_BAD_REQUEST),
        ("delete", "organizer", None, status.HTTP_204_NO_CONTENT),
        ("delete", "admin", None, status.HTTP_204_NO_CONTENT),
        ("delete", "non_organizer", None, status.HTTP_403_FORBIDDEN),
    ],
)
def test_delete_ticket_permissions(
    api_client,
    create_ticket,
    create_event,
    create_user,
    method,
    user_type,
    data,
    expected_status,
):
    organizer = create_user("organizer")
    event = create_event(organizer=organizer)

    if user_type == "organizer":
        current_user = organizer
    elif user_type == "admin":
        current_user = create_user("admin", is_staff=True)
    elif user_type == "non_organizer":
        current_user = create_user("non_organizer")
    else:
        current_user = None

    if current_user:
        api_client.force_authenticate(user=current_user)

    ticket = create_ticket(event=event)
    url = reverse("ticket-detail", args=[ticket.id])

    if method == "patch":
        response = api_client.patch(url, data=data, format="json")
    elif method == "delete":
        response = api_client.delete(url)

    assert response.status_code == expected_status

    if method == "patch" and expected_status == status.HTTP_200_OK:
        ticket.refresh_from_db()
        assert ticket.price == data.get("price")
    elif method == "delete" and expected_status == status.HTTP_204_NO_CONTENT:
        assert Ticket.objects.count() == 0
