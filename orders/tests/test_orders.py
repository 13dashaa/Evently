import pytest
from django.urls import reverse
from rest_framework import status

from orders.models import Order


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_authenticated, expected_result, expected_order_count",
    [
        (True, status.HTTP_201_CREATED, 1),
        (False, status.HTTP_403_FORBIDDEN, 0),
    ],
)
def test_create_order_with_different_auth_states(
    api_client,
    create_ticket,
    create_user,
    order_data,
    is_authenticated,
    expected_result,
    expected_order_count,
):
    user = create_user("customer")

    if is_authenticated:
        api_client.force_authenticate(user=user)

    url = reverse("order-list")
    response = api_client.post(url, data=order_data, format="json")

    assert response.status_code == expected_result
    assert Order.objects.count() == expected_order_count

    if is_authenticated:
        order = Order.objects.get()
        assert order.user == user


@pytest.mark.django_db
def test_list_orders_by_owner_success(api_client, create_ticket, create_user, create_order):
    user1 = create_user("customer1")
    user2 = create_user("customer2")
    ticket = create_ticket()
    create_order(ticket=ticket, user=user1, quantity=1)
    create_order(ticket=ticket, user=user2, quantity=3)

    api_client.force_authenticate(user=user1)

    url = reverse("order-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["user"] == user1.id


@pytest.mark.django_db
def test_retrieve_order_by_owner_success(api_client, create_ticket, create_user, create_order):
    owner = create_user("customer1")
    ticket = create_ticket()
    order = create_order(ticket=ticket, user=owner, quantity=1)

    api_client.force_authenticate(user=owner)

    url = reverse("order-detail", args=[order.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"] == owner.id


@pytest.mark.django_db
def test_retrieve_order_by_non_owner_failure(api_client, create_ticket, create_user, create_order):
    owner = create_user("customer1")
    non_owner = create_user("customer2")
    ticket = create_ticket()
    order = create_order(ticket=ticket, user=owner, quantity=1)

    api_client.force_authenticate(user=non_owner)

    url = reverse("order-detail", args=[order.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    "http_methods",
    [
        "patch",
        "delete",
    ],
)
def test_forbidden_order_methods_failure(api_client, create_user, create_order, http_methods):
    user = create_user("customer1")
    order = create_order(user=user, quantity=1)

    api_client.force_authenticate(user=user)
    url = reverse("order-detail", args=[order.id])

    if http_methods == "patch":
        response = api_client.patch(url, data={"quantity": 2}, format="json")
    elif http_methods == "delete":
        response = api_client.delete(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
