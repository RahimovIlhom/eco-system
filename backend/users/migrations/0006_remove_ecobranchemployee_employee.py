# Generated by Django 5.0.7 on 2024-07-20 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_ecobranchemployee_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ecobranchemployee',
            name='employee',
        ),
    ]