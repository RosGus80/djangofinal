import os

from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='rosgus80@gmail.com',
            name='Admin',
            phone='+7 917 942 1479',
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(os.getenv('ADMIN_PASSWORD'))
        user.save()

