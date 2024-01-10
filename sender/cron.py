from django.core.mail import send_mail
from django.utils.datetime_safe import datetime

from sender.models import MassSend


def my_scheduled_job():
    print('yes')

