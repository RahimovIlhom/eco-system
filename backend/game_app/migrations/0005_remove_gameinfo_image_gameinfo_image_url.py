# Generated by Django 5.0.7 on 2024-07-26 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0004_gameinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameinfo',
            name='image',
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='image_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
