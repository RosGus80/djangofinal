from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    name = models.CharField(max_length=50, verbose_name='Имя пользователя')

    is_verified = models.BooleanField(default=False, verbose_name="Подтвержден")

    phone = PhoneNumberField(**NULLABLE, default="", verbose_name='Номер телефона (опционально)')

    verification_code = models.CharField(max_length=10, default="", verbose_name='Код подтверждения')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

