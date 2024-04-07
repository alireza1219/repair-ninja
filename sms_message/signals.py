from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from repair_core.models import Service
from sms_message.utils import SmsMessage

# FIXME: Use pre_save signal to prevent duplication messages.


@receiver(post_save, sender=Service)
def notify_customer(sender, instance, created, **kwargs):
    """Notify customer on service creation or update."""
    # Do nothing when sms messages are not enabled or the API key is empty.
    if not settings.SMS_ENABLED or not settings.SMS_API_KEY:
        return

    customer = instance.customer
    customer_fullname = str(customer).strip() or 'Customer'
    customer_phone = customer.phone
    message = f"Dear {customer_fullname},\n"
    if instance.service_status == Service.SERVICE_RECEIVED:
        message += (
            'Your service has been received.\n'
            f'The estimated delivery date is: {instance.estimation_delivery}.'
        )
    elif instance.service_status == Service.SERVICE_IN_PROGRESS:
        message += "Your service is currently being processed."
    elif instance.service_status == Service.SERVICE_COMPLETED:
        message += "Your service has been completed and is now ready to receive."
    elif instance.service_status == Service.SERVICE_DELIVERED:
        message += "Thanks for choosing us! We hope to see you again."

    sms_instance = SmsMessage()
    sms_instance.send_sms(number=customer_phone, message=message)
