import smtplib

from django.core.mail import send_mail
from django.utils.datetime_safe import datetime
import datetime as dt

from sender.models import MassSend, Log


# def write_logs(text):
#     with open('/tmp/log.log', 'w') as file:
#         file.write(text+'\n')


def send():

    log_owner = None
    log_send = None
    log_date = None
    log_is_sent = None

    tasks = MassSend.objects.filter(is_active=True, banned=False)

    for task in tasks:
        log_owner = task.owner
        log_date = datetime.today()
        log_send = task
        print(f'{datetime.today()}: Working on "{task.name}"')

        if task.owner.is_verified and not task.owner.is_blocked:
            if task.start_date <= datetime.today().date() <= task.end_date:

                print(f'{datetime.today()}: Sending "{task.name}"')

                for client in task.group.clients.all():
                    try:
                        send_mail(
                            subject=task.subject,
                            message=task.body,
                            from_email='noreply@gmail.com',
                            recipient_list=[client.email],
                            fail_silently=False
                        )
                        print(f'{datetime.today()}: Successfully sent {task.name} email to {client.email}')
                    except smtplib.SMTPDataError:
                        log_is_sent = False
                        print(f'{datetime.today()}: Failed to send {task.name} email to {client.email}')

                if task.periodicity == '1':
                    new_start_date = task.start_date + dt.timedelta(days=1)
                    new_end_date = new_start_date + dt.timedelta(days=1)
                    MassSend.objects.filter(pk=task.pk).update(start_date=new_start_date, end_date=new_end_date)
                    print(f'{datetime.today()}: Changed "{task.name}" start date to {new_start_date}')
                elif task.periodicity == '7':
                    new_start_date = task.start_date + dt.timedelta(days=7)
                    new_end_date = new_start_date + dt.timedelta(days=1)
                    MassSend.objects.filter(pk=task.pk).update(start_date=new_start_date, end_date=new_end_date)
                    print(f'{datetime.today()}: Changed "{task.name}" start date to {new_start_date}')
                else:
                    new_start_date = task.start_date + dt.timedelta(days=30)
                    new_end_date = new_start_date + dt.timedelta(days=1)
                    MassSend.objects.filter(pk=task.pk).update(start_date=new_start_date, end_date=new_end_date)
                    print(f'{datetime.today()}: Changed "{task.name}" start date to {new_start_date}')

                print(f'{datetime.today()} "{task.name}" completed')
                log_is_sent = True
                new_log = Log.objects.create(
                    date=log_date,
                    is_sent=log_is_sent,
                    send=log_send,
                    owner=log_owner
                )
                print(f'{datetime.today()} {new_log} log created\n\n')

            else:
                print(f'{datetime.today()} "{task.name}" sending date is not today\n\n')
        else:
            print(f'{datetime.today()} "{task.name}" owner is not verified/blocked\n\n')
