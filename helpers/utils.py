from datetime import timedelta
from fastnanoid import generate
from itertools import islice
from jwt import encode
from random import randint
from time import sleep
from typing import Any

from django.conf import settings
from django.utils.timezone import now
from rest_framework.utils.serializer_helpers import ReturnDict

from helpers.types import EmailMessage
from tasks.task_email import task_send_email, task_send_mass_email


def generate_oid(length: int = 21):
    """Generates unique value with NanoID of given length."""
    return generate(size=length)


def generate_token(data: dict[str, Any] | ReturnDict[str, Any]):
    """Generates JWT token with given data."""
    time = now()

    encoded_token = encode(
        {
            **data,
            'exp': (time + timedelta(hours=settings.JWT_EXP_HOURS)).timestamp(),
            'iat': time.timestamp()
        },
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_token


def generate_otp():
    """Generates OTP with given length."""
    return randint(100000, 999999)


def split_into_chunks(data: list[Any], chunk_size: int):
    """Yield successive chunks from `data`. Returns a list of lists."""
    it = iter(data)
    for _ in range(0, len(data), chunk_size):
        yield list(islice(it, chunk_size))


def send_email(email: EmailMessage, fail_silently: bool = False):
    """Customized function to send an email, asynchronously."""
    task_send_email.delay(
        subject=email.subject,
        body=email.body,
        from_email=email.from_email,
        to=email.to,
        fail_silently=fail_silently
    )


def send_mass_email(emails: list[EmailMessage], fail_silently: bool = False):
    """Send emails in bulk, each message to each recipients. Runs asynchronously."""
    datatuple: list[tuple[str, str, str, list[str]]] = []

    for email in emails:
        datatuple.append((
            email.subject,
            email.body,
            email.from_email if email.from_email else settings.DEFAULT_FROM_EMAIL,
            email.to
        ))

    task_send_mass_email.delay(datatuple=datatuple, fail_silently=fail_silently)


def send_mass_email_cluster(emails: list[EmailMessage], per_cluster: int = 250, fail_silently: bool = False, delay: int = 0):
    """Clustered mass email sending, useful for very large amount of emails to avoid limits."""
    for chunk in split_into_chunks(emails, per_cluster):
        datatuple = [
            (
                email.subject,
                email.body,
                email.from_email if email.from_email else settings.DEFAULT_FROM_EMAIL,
                email.to
            ) for email in chunk
        ]

        task_send_mass_email.delay(datatuple=datatuple, fail_silently=fail_silently)

        if delay > 0:
            sleep(delay)
