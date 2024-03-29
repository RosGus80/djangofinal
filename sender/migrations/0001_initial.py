# Generated by Django 4.2.7 on 2024-01-06 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('full_name', models.CharField(default='', max_length=50, verbose_name='Имя')),
            ],
        ),
        migrations.CreateModel(
            name='ClientGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название группы')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата попытки')),
                ('is_sent', models.BooleanField(verbose_name='Статус отправки')),
                ('server_response', models.IntegerField(verbose_name='Ответ сервера')),
            ],
        ),
        migrations.CreateModel(
            name='MassSend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=150, verbose_name='Название рассылки')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активна')),
                ('subject', models.CharField(max_length=70, verbose_name='Тема письма')),
                ('body', models.TextField(verbose_name='Содержание письма')),
                ('start_date', models.DateField(verbose_name='Дата рассылки')),
                ('end_date', models.DateField(verbose_name='Последняя дата попытки')),
                ('periodicity', models.CharField(choices=[('1', 'Every day'), ('7', 'Every week'), ('30', 'Every month')], default='', max_length=300)),
                ('group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sender.clientgroup', verbose_name='Группа рассылки')),
            ],
        ),
    ]
