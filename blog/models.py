from django.db import models

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')

    image = models.ImageField(upload_to='static/previews/', **NULLABLE, verbose_name='Картинка')

    views = models.IntegerField(default=0, verbose_name='Просмотры')
    date = models.DateField(auto_now=True, verbose_name='Дата публикации')

