# Generated by Django 5.0.7 on 2024-07-27 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_registeredqrcode_winner_delete_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='suggested',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.participant'),
        ),
    ]
