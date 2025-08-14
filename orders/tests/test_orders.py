import pytest
from django.urls import reverse
from rest_framework import serializers, status

from orders.models import Order, PaidStatus
from orders.serializers import OrderSerializer


@pytest.mark.django_db
def test_create_order_by_authenticated_user_success(
    api_client, create_ticket, create_user, order_data
):
    customer = create_user("customer")
    api_client.force_authenticate(user=customer)
    # ticket = create_ticket(available_quantity=100, quantity=100)

    url = reverse("order-list")
    response = api_client.post(url, data=order_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Order.objects.count() == 1
    assert Order.objects.get().quantity == order_data.get("quantity")


@pytest.mark.django_db
def test_create_order_by_unauthenticated_user_failure(api_client, order_data):
    url = reverse("order-list")
    response = api_client.post(url, data=order_data, format="json")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Order.objects.count() == 0


@pytest.mark.django_db
def test_list_orders_by_owner_success(
    api_client, create_ticket, create_user, create_order
):
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
def test_retrieve_order_by_owner_success(
    api_client, create_ticket, create_user, create_order
):
    owner = create_user("customer1")
    ticket = create_ticket()
    order = create_order(ticket=ticket, user=owner, quantity=1)

    api_client.force_authenticate(user=owner)

    url = reverse("order-detail", args=[order.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"] == owner.id


@pytest.mark.django_db
def test_retrieve_order_by_non_owner_failure(
    api_client, create_ticket, create_user, create_order
):
    owner = create_user("customer1")
    non_owner = create_user("customer2")
    ticket = create_ticket()
    order = create_order(ticket=ticket, user=owner, quantity=1)

    api_client.force_authenticate(user=non_owner)

    url = reverse("order-detail", args=[order.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_order_failure(api_client, create_user, create_order):
    user = create_user("customer1")
    order = create_order(user=user, quantity=1)

    api_client.force_authenticate(user=user)
    url = reverse("order-detail", args=[order.id])
    data = {"quantity": 2}
    response = api_client.patch(url, data=data, format="json")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_delete_order_failure(api_client, create_user, create_order):
    user = create_user("customer1")
    order = create_order(user=user, quantity=1)

    api_client.force_authenticate(user=user)
    url = reverse("order-detail", args=[order.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
