# Generated by Django 5.0.7 on 2024-07-17 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecobranchemployee',
            name='language',
            field=models.CharField(choices=[('uz', 'Uzbek'), ('ru', 'Russian')], default='uz', max_length=2),
        ),
        migrations.AddField(
            model_name='participant',
            name='language',
            field=models.CharField(choices=[('uz', 'Uzbek'), ('ru', 'Russian')], default='uz', max_length=2),
        ),
    ]
