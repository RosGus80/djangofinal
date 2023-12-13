from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='mail')
    name = models.CharField(verbose_name='username')

    verified = False

    phone = PhoneNumberField(**NULLABLE, verbose_name='phone number')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

