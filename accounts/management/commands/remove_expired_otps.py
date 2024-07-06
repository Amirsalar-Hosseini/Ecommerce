from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Remove expired otps'

    def handle(self, *args, **options):
        expired_time = datetime.now() - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write(self.style.SUCCESS('Successfully removed expired otps'))