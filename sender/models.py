from django.db import models

from users.models import User


NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Client(models.Model):
    email = models.EmailField(verbose_name='client_email')
    description = models.TextField(**NULLABLE, verbose_name='desc')
    full_name = models.CharField(default='', verbose_name='fio')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='owner')


class ClientGroup(models.Model):
    name = models.CharField(max_length=150, verbose_name='name of group')
    clients = models.ManyToManyField(Client, verbose_name='clients')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='owner')


class MassSend(models.Model):

    name = models.CharField(default='', max_length=150, verbose_name='name')

    subject = models.CharField(max_length=70, verbose_name='subject')
    body = models.TextField(verbose_name='email body')

    start_date = models.DateField(verbose_name='start date')
    end_date = models.DateField(verbose_name='end date')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='owner')
    group = models.ForeignKey(ClientGroup, on_delete=models.CASCADE, default=None, verbose_name='group')


