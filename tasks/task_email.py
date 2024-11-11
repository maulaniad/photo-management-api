from celery import Task, shared_task

from django.conf import settings
from django.core.mail import send_mail, get_connection, EmailMultiAlternatives


Task.__class_getitem__ = classmethod(lambda cls, *args, **kwargs: cls) # type: ignore[attr-defined]

@shared_task(bind=True)
def task_send_email(self: Task, subject: str, body: str, from_email: str | None, to: list[str], fail_silently: bool = False):
    self.update_state(state="RUNNING", meta={})

    try:
        send_mail(
            subject=subject,
            message=body,
            html_message=body,
            from_email=from_email,
            recipient_list=to,
            fail_silently=fail_silently
        )
    except Exception as e:
        self.update_state(state="FAILURE", meta={'exc': str(e)})
        return False

    self.update_state(state="SUCCESS", meta={})
    return True


@shared_task(bind=True)
def task_send_mass_email(self: Task, datatuple: list[tuple[str, str, str, list[str]]], fail_silently: bool = False):
    self.update_state(state="RUNNING", meta={})

    try:
        connection = get_connection(username=settings.EMAIL_HOST_USER,
                                    password=settings.EMAIL_HOST_PASSWORD,
                                    fail_silently=fail_silently)
        html_messages = []
        for subject, body, from_email, recipient in datatuple:
            message = EmailMultiAlternatives(subject, body, from_email, recipient)
            message.attach_alternative(body, 'text/html')
            html_messages.append(message)

        connection.send_messages(html_messages)
    except Exception as e:
        self.update_state(state="FAILURE", meta={'exc': str(e)})
        return False

    self.update_state(state="SUCCESS", meta={})
    return True
