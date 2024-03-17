import random
from datetime import timedelta

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

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
