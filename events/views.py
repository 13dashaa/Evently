from django.shortcuts import render
from rest_framework import viewsets

from events.models import Event, Venue
from events.serializers import EventSerializer, VenueSerializer


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
