from django.shortcuts import render
from rest_framework import viewsets

from events.models import Venue
from events.serializers import VenueSerializer


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
