from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter

from orders.models import Order, Ticket
from orders.permissions import IsTicketOrganizerOrAdminOrReadOnly
from orders.serializers import OrderSerializer, TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsTicketOrganizerOrAdminOrReadOnly]

    def perform_create(self, serializer):
        event = serializer.validated_data.get("event")
        if event.organizer != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Ticket can only be made by an organizer or admin.")
        serializer.save(available_quantity=serializer.validated_data.get("quantity"))


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "head", "options"]
    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = ["status", "ticket__event__name"]
    ordering_fields = ["created_at", "status"]
    ordering = ["-created_at"]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
