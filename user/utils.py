import logging


from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail, mail_admins


logger = logging.getLogger(__name__)


def send_email_with_html_body(
    subjet: str, recevers: list, template: str, context: dict
):  # template: str,
    """This function help to send a customize to specific user or set of users."""
    print(
        f"Appel function 🍿  {settings.EMAIL_HOST_USER}| {subjet} | {recevers} | {context} | {template} "
    )
    try:
        message = render_to_string(template, context)
        # a = 1
        send_mail(
            subject=subjet,
            message=message,  # message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recevers,
            fail_silently=False,
            html_message=message,
        )

        print("MAIL SENT WITH SUCCES")

        return True

    except Exception as e:
        print("Error in send mail", e)
        logger.error(e)

    return False


def send_email_with_html_body_to_admin(subject: str, message: str):
    """
    This function send email to admin user

    #
    """
    try:
        mail_admins()
    except Exception as e:
        logger.warning(e)
