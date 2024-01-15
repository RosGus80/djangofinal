from django import forms
from django.db import models

from users.models import User


NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Client(models.Model):
    email = models.EmailField(verbose_name='Почта')
    description = models.TextField(**NULLABLE, verbose_name='Комментарий')
    full_name = models.CharField(max_length=50, default='', verbose_name='Имя')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='Пользователь')


class ClientGroup(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название группы')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты группы')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='Пользователь')


class MassSend(models.Model):

    CHOICES = [
        ('1', 'Каждый день'),
        ('7', 'Каждую неделю'),
        ('30', 'Каждый месяц'),
    ]

    name = models.CharField(default='', max_length=150, verbose_name='Название рассылки')

    is_active = models.BooleanField(default=False, verbose_name='Активна')
    banned = models.BooleanField(default=False, verbose_name='Заблокирована')

    subject = models.CharField(max_length=70, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Содержание письма')

    start_date = models.DateField(verbose_name='Дата рассылки')
    end_date = models.DateField(verbose_name='Последняя дата попытки')

    periodicity = models.CharField(max_length=300, choices=CHOICES, default='', verbose_name='Периодичность рассылки')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='Пользователь')
    group = models.ForeignKey(ClientGroup, on_delete=models.CASCADE, default=None, verbose_name='Группа рассылки')


class Log(models.Model):
    date = models.DateField(verbose_name='Дата попытки')

    is_sent = models.BooleanField(verbose_name='Статус отправки')

    send = models.ForeignKey(MassSend, on_delete=models.CASCADE, verbose_name='Рассылка')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None, verbose_name='Пользователь')

