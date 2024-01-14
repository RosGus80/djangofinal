import smtplib

from django.core.mail import send_mail
from django.utils.datetime_safe import datetime

from sender.models import MassSend, Log


def write_logs(text):
    with open('tmp/log.log', 'w') as file:
        file.write(text+'\n')


def send():

    tasks = MassSend.objects.filter(is_active=True, banned=False)

    for task in tasks:
        if task.owner.is_verified and not task.owner.is_blocked:
            if task.start_date <= datetime.today().date() <= task.end_date:
                for i in range(len(task.group.clients.all())+1):
                    try:
                        send_mail(
                            subject=task.subject,
                            message=task.body,
                            from_email='noreply@gmail.com',
                            recipient_list=[task.group.clients.all()[i].email],
                            fail_silently=False
                        )
                    except smtplib.SMTPDataError:
                        write_logs(f'{datetime.today()} Failed to send email to {task.group.clients.all()[i].email}')

                if task.periodicity == '1':
                    task.start_date += datetime.timedelta(days=1)
                    task.end_date = task.start_date + datetime.timedelta(days=1)
                    task.save(commit=True)
                elif task.periodicity == '7':
                    task.start_date += datetime.timedelta(days=7)
                    task.end_date = task.start_date + datetime.timedelta(days=1)
                    task.save(commit=True)
                else:
                    task.start_date += datetime.timedelta(days=30)
                    task.end_date = task.start_date + datetime.timedelta(days=1)
                    task.save(commit=True)

                write_logs(f'{datetime.today()} {task.name} completed')

            else:
                write_logs(f'{datetime.today()} {task.name} skipped')
        else:
            write_logs(f'{datetime.today()} {task.name} owner is not verified/blocked')
