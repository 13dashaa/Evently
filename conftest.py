import uuid

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from events.models import Event, Venue
from orders.models import Ticket, TicketType


@pytest.fixture
def create_user():
    def _create_user(username: str, password: str = "password123", **kwargs) -> User:
        unique_username = f"{username}_{uuid.uuid4().hex[:8]}"
        return User.objects.create_user(
            username=unique_username, password=password, **kwargs
        )

    return _create_user


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
def event_data(create_venue) -> dict:
    venue = create_venue()
    return {
        "name": "Test event",
        "description": "Test description",
        "date": "2025-01-01",
        "venue": venue.id,
    }


@pytest.fixture
def create_venue():
    def _create_venue(**kwargs) -> Venue:
        return Venue.objects.create(
            name=kwargs.get("name", "Test Venue"),
            address=kwargs.get("address", "Test Address"),
            capacity=kwargs.get("capacity", 100),
        )

    return _create_venue


@pytest.fixture
def create_event(create_user, create_venue):
    def _create_event(organizer=None, **kwargs) -> Event:
        if organizer is None:
            organizer = create_user("default_organizer")
        venue = create_venue()
        return Event.objects.create(
            name=kwargs.get("name", "Test event"),
            description=kwargs.get("description", "Test description"),
            date=kwargs.get("date", "2025-01-01"),
            venue=venue,
            organizer=organizer,
        )

    return _create_event


@pytest.fixture
def ticket_data(create_event) -> dict:
    event = create_event()
    return {
        "event": event.id,
        # "type": "standard",
        "price": 500.00,
        "quantity": 100,
        "available_quantity": 100,
    }


@pytest.fixture
def create_ticket(create_event):
    def _create_ticket(event=None, **kwargs) -> Ticket:
        if event is None:
            event = create_event()
        return Ticket.objects.create(
            event=event,
            price=kwargs.get("price", 1000),
            quantity=kwargs.get("quantity", 10000),
            type=kwargs.get("type", TicketType.standard),
            available_quantity=kwargs.get("available_quantity", 10000),
        )

    return _create_ticket
