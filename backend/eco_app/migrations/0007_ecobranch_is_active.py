# Generated by Django 5.0.7 on 2024-08-01 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco_app', '0006_ecobranch_information_ru_ecobranch_information_uz_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecobranch',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
