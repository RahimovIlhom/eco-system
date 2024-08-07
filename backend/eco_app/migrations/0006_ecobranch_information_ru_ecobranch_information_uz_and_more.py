# Generated by Django 5.0.7 on 2024-07-21 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eco_app', '0005_remove_ecobranch_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecobranch',
            name='information_ru',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ecobranch',
            name='information_uz',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ecobranch',
            name='name_ru',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ecobranch',
            name='name_uz',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
