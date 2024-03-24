import random
import re

from datetime import timedelta
from smtplib import SMTPException

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils import timezone
from django.utils.html import strip_tags

from .models import OTP


def generate_otp(instance):
    """
    Generate a new OTP for the given instance.
    """
    try:
        # Prevent duplicate OTP requests before the current OTP expiration.
        otp_obj = OTP.objects.get(
            content_type=ContentType.objects.get_for_model(instance.__class__),
            object_id=instance.pk,
            expires_at__gt=timezone.now(),
        )

        return otp_obj.otp
    except OTP.DoesNotExist:
        otp = ''.join(random.choices('0123456789', k=6))

        # TODO: Configurable expire time would be nice to have :)?
        expires_at = timezone.now() + timedelta(minutes=2)

        OTP.objects.create(
            content_object=instance,
            otp=otp,
            expires_at=expires_at,
        )

        return otp


def verify_otp(instance, otp):
    """
    Verify the OTP for the given instance.
    """
    try:
        otp_obj = OTP.objects.get(
            content_type=ContentType.objects.get_for_model(instance.__class__),
            object_id=instance.pk,
            expires_at__gt=timezone.now(),
        )
    except OTP.DoesNotExist:
        return False

    if otp_obj.otp == otp:
        # Remove the OTP object after validation success.
        otp_obj.delete()

        return True

    return False


def send_otp_email(instance, otp: str):
    """
    Email the OTP.
    """
    subject = 'OTP Verification'
    from_email = settings.DEFAULT_FROM_EMAIL
    to = instance.email

    template = get_template('emails/email_template.html')
    html_message = template.render({
        'customer': {
            'first_name': instance.first_name,
            'last_name': instance.last_name
        },
        'otp': otp
    })
    # This is useful for the older email clients with no HTML support.
    plain_message = strip_tags_extended(html_message)

    try:
        # https://docs.djangoproject.com/en/5.0/topics/email/#django.core.mail.EmailMessage
        email = EmailMultiAlternatives(
            subject,
            plain_message,
            from_email,
            [to]
        )
        email.attach_alternative(html_message, 'text/html')
        email.send()
    except SMTPException:
        # https://docs.python.org/3/library/smtplib.html#smtplib.SMTPException
        # TODO: Logging.
        pass


def strip_tags_extended(html):
    """
    An extended version of the strip_tags() function.
    https://docs.djangoproject.com/en/5.0/ref/utils/#django.utils.html.strip_tags
    """
    # Replace the <head> section with an empty string.
    cleaned_html = re.sub(
        r'<head\b[^>]*>.*?</head>',
        '',
        html,
        flags=re.DOTALL | re.IGNORECASE
    )
    # Remove continuous whitespaces and html tags.
    text = re.sub('[ \t]+', ' ', strip_tags(cleaned_html))
    # Strip single spaces in the beginning of each line.
    return text.replace('\n ', '\n').strip()
