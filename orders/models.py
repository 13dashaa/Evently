from django.db import models


class TicketType(models.TextChoices):
    standard = "standard"
    vip = "vip"
    early_bird = "early bird"


class PaidStatus(models.TextChoices):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    cancelled = "cancelled"
    refunded = "refunded"


class Ticket(models.Model):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    type = models.CharField(choices=TicketType, default=TicketType.standard)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField()
    available_quantity = models.IntegerField()


class Order(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(choices=PaidStatus, default=PaidStatus.pending)
    created_at = models.DateTimeField(auto_now_add=True)
