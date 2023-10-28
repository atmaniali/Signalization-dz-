import logging


from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail, mail_admins


logger = logging.getLogger(__name__)


def send_email_with_html_body(
    subjet: str, recevers: list, template: str, context: dict
):
    """This function help to send a customize to specific user or set of users."""

    try:
        message = render_to_string(template, context)

        send_mail(
            subject=subjet,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recevers,
            fail_silently=True,
            html_message=message,
        )

        return True

    except Exception as e:
        logger.error(e)

    return False


def send_email_with_html_body_to_admin(subject: str, message: str):
    """This function send email to admin user"""
    try:
        mail_admins()
    except Exception as e:
        logger.warning(e)
