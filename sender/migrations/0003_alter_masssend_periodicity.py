# Generated by Django 4.2.7 on 2024-01-10 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='masssend',
            name='periodicity',
            field=models.CharField(choices=[('1', 'Каждый день'), ('7', 'Каждую неделю'), ('30', 'Каждый месяц')], default='', max_length=300, verbose_name='Периодичность рассылки'),
        ),
    ]
