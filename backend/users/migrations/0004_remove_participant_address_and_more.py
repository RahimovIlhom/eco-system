# Generated by Django 5.0.7 on 2024-07-17 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='address',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='location',
        ),
    ]
