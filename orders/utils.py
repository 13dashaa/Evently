import aioboto3

from eventservice.config import settings


async def get_client() -> aioboto3.Session.client:
    session = aioboto3.Session()
    return session.client(
        settings.SERVICES,
        endpoint_url=settings.ENDPOINT_URL,
        region_name=settings.AWS_DEFAULT_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def create_message(subject_data: str, text: str) -> dict:
    message = {
        "Subject": {"Data": subject_data, "Charset": "UTF-8"},
        "Body": {
            "Text": {
                "Data": text,
                "Charset": "UTF-8",
            },
        },
    }

    return message


async def send_email(
    client: aioboto3.Session.client,
    email: str,
    message: dict,
    sender: str = settings.SENDER,
) -> None:
    await client.verify_email_identity(EmailAddress=sender)
    await client.send_email(
        Source=sender,
        Destination={
            "ToAddresses": email,
        },
        Message=message,
    )
