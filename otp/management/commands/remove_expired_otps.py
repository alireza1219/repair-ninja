from django.core.management.base import BaseCommand
from django.utils import timezone

from otp.models import OTP


class Command(BaseCommand):
    help = 'Remove expired OTPs from the database'

    def handle(self, *args, **options):
        expired_otps = OTP.objects.filter(expires_at__lt=timezone.now())
        num_deleted, _ = expired_otps.delete()
        self.stdout.write(self.style.SUCCESS(
            f'Removed {num_deleted} expired OTPs from the database.'))
