# Generated by Django 5.0.7 on 2024-08-01 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address_app', '0003_address_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_ru',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='address_uz',
            field=models.TextField(blank=True, null=True),
        ),
    ]