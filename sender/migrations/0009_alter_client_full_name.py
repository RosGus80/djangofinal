# Generated by Django 4.2.7 on 2023-12-06 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0008_alter_masssend_end_date_alter_masssend_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='full_name',
            field=models.CharField(default='', verbose_name='fio'),
        ),
    ]
