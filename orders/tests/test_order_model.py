import pytest
from django.template.context_processors import request
from rest_framework import serializers, test

from orders.exeptions import CreateOrderException
from orders.models import PaidStatus
from orders.serializers import OrderSerializer


@pytest.mark.django_db
def test_create_order_success(create_ticket, create_user):
    user = create_user("customer")
    ticket = create_ticket(available_quantity=100, quantity=100, price=50.0)
    order_data = {
        "user": user.id,
        "ticket": ticket.id,
        "quantity": 5,
    }

    test_request = test.APIRequestFactory().get("/")
    test_request.user = user
    context = {"request": test_request}

    serializer = OrderSerializer(data=order_data, context=context)
    assert serializer.is_valid()
    order = serializer.save()

    assert order.user == user
    assert order.ticket == ticket
    assert order.quantity == 5
    assert order.total_price == 250.0
    assert order.status == PaidStatus.pending

    ticket.refresh_from_db()
    assert ticket.available_quantity == ticket.quantity - order.quantity


@pytest.mark.django_db
def test_create_order_insufficient_tickets_failure(create_ticket, create_user):
    user = create_user("customer")
    ticket = create_ticket(available_quantity=5, quantity=100, price=50.0)
    order_data = {
        "user": user.id,
        "ticket": ticket.id,
        "quantity": 10,
    }

    test_request = test.APIRequestFactory().get("/")
    test_request.user = user
    context = {"request": test_request}

    serializer = OrderSerializer(data=order_data, context=context)

    assert serializer.is_valid()
    with pytest.raises(CreateOrderException):
        serializer.save(raise_exception=True)


@pytest.mark.django_db
def test_create_order_invalid_amount(create_ticket, create_user):
    user = create_user("customer")
    ticket = create_ticket(available_quantity=5, quantity=100, price=50.0)
    order_data = {
        "user": user.id,
        "ticket": ticket.id,
        "quantity": -10,
    }
    test_request = test.APIRequestFactory().get("/")
    test_request.user = user
    context = {"request": test_request}

    serializer = OrderSerializer(data=order_data, context=context)
    assert not serializer.is_valid()
