import smtplib

from django.core.mail import send_mail
from django.utils.datetime_safe import datetime
import datetime as dt

from sender.models import MassSend, Log


# def write_logs(text):
#     with open('/tmp/log.log', 'w') as file:
#         file.write(text+'\n')


def send():

    tasks = MassSend.objects.filter(is_active=True, banned=False)

    for task in tasks:
        if task.owner.is_verified and not task.owner.is_blocked:
            if task.start_date <= datetime.today().date() <= task.end_date:
                for client in task.group.clients.all():
                    try:
                        send_mail(
                            subject=task.subject,
                            message=task.body,
                            from_email='noreply@gmail.com',
                            recipient_list=[client.email],
                            fail_silently=False
                        )
                    except smtplib.SMTPDataError:
                        print(f'{datetime.today()} Failed to send email to {task.group.clients.all()[i].email}')

                print(task)

                if task.periodicity == '1':
                    print(MassSend.objects.get(pk=task.pk).start_date)
                    MassSend.objects.filter(pk=task.pk).update(start_date=task.start_date + dt.timedelta(days=1),
                                                               end_date=task.end_date + dt.timedelta(days=1))
                elif task.periodicity == '7':
                    MassSend.objects.filter(pk=task.pk).update(start_date=task.start_date + dt.timedelta(days=1),
                                                               end_date=task.end_date + dt.timedelta(days=1))
                else:
                    print('30 worked out)')
                    MassSend.objects.filter(pk=task.pk).update(start_date=task.start_date + dt.timedelta(days=1),
                                                               end_date=task.end_date + dt.timedelta(days=1))

                print(f'{datetime.today()} {task.name} completed')

            else:
                print(f'{datetime.today()} {task.name} skipped')
        else:
            print(f'{datetime.today()} {task.name} owner is not verified/blocked')
