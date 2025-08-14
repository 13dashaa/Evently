import asyncio

from botocore.exceptions import (
    ClientError,
    EndpointConnectionError,
    NoCredentialsError,
    ParamValidationError,
)
from celery import shared_task

from eventservice.config import settings
from orders.models import Order
from orders.utils import create_message, get_client, send_email


@shared_task
async def handle_send_order_confirmation_notification(order_id: int):
    try:
        order = Order.objects.get(id=order_id)
        user = order.user

        recipient = user.email

        message = create_message(
            subject_data=f"Order Confirmation #{order_id}",
            text=(
                f"Hello, {user.username}!\n\n"
                f'Your order for the event "{order.ticket.event.name}" '
                f"has been successfully created.\n"
                f"Number of tickets: {order.quantity}\n"
                f"Total price: {order.total_price}\n\n"
                "Thank you for your purchase!"
            ),
        )

        for attempt in range(settings.MAX_TRIES):
            try:
                async with await get_client() as client:
                    await send_email(client=client, email=recipient, message=message)
                return
            except (
                NoCredentialsError,
                EndpointConnectionError,
                ClientError,
                ParamValidationError,
            ):
                if attempt < settings.MAX_TRIES - 1:
                    await asyncio.sleep(1)
                else:
                    return
    except Order.DoesNotExist:
        return f"Order with id {order_id} does not exist."


@shared_task
def send_order_confirmation_notification(order_id: int):
    asyncio.run(handle_send_order_confirmation_notification(order_id=order_id))
