import smtplib

from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils.datetime_safe import datetime
from datetime import timedelta

from sender.models import MassSend, Log


class Command(BaseCommand):

    def handle(self, *args, **options):
        tasks = MassSend.objects.filter(is_active=True)

        for task in tasks:
            if task.start_date <= datetime.today().date() <= task.end_date:
                for i in range(len(task.group.clients.all())):
                    try:
                        send_mail(
                            subject=task.subject,
                            message=task.body,
                            from_email='noreply@gmail.com',
                            recipient_list=[task.group.clients.all()[i].email],
                            fail_silently=False
                        )
                    except smtplib.SMTPDataError:
                        Log.objects.create(date=datetime.today(), is_sent=False, server_response=0,
                                           send=task, owner=task.owner)
                    finally:
                        Log.objects.create(date=datetime.today(), is_sent=True, server_response=1,
                                           send=task, owner=task.owner)

                print(task.group.clients.all().values_list('email', flat=True))

                print(f'{task.name} completed')


