# Generated by Django 5.0.7 on 2024-07-20 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='employee',
        ),
    ]