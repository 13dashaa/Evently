from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from orders.models import Ticket
from orders.permissions import IsTicketOrganizerOrAdminOrReadOnly
from orders.serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsTicketOrganizerOrAdminOrReadOnly]

    def perform_create(self, serializer):
        event = serializer.validated_data.get("event")
        if event.organizer != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Ticket can only be made by an organizer or admin.")
        serializer.save(available_quantity=serializer.validated_data.get("quantity"))
