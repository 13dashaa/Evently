from django.db import transaction
from rest_framework import serializers

from orders.exeptions import CreateOrderException, NotAuthenticatedException
from orders.models import Order, Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ["id", "available_quantity"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["total_price", "status", "created_at", "user"]

    def validate(self, data):
        user = self.context["request"].user

        if not user.is_authenticated:
            raise NotAuthenticatedException("You are not authenticated.")
        # quantity = data["quantity"]
        # ticket = data["ticket"]
        #
        # if quantity > ticket.available_quantity:
        #     raise CreateOrderException("Not enough available ticket.")

        data["user"] = user

        return data

    def create(self, validated_data):
        quantity = validated_data.get("quantity")
        ticket = validated_data.get("ticket")

        with transaction.atomic():
            ticket = Ticket.objects.select_for_update().get(pk=ticket.pk)

            if quantity > ticket.available_quantity:
                raise CreateOrderException("Not enough available ticket.")

            total_price = quantity * ticket.price

            validated_data["total_price"] = total_price

            ticket.available_quantity -= quantity
            ticket.save()

            order = Order.objects.create(
                user=validated_data["user"],
                total_price=total_price,
                quantity=quantity,
                ticket=ticket,
            )

        return order
