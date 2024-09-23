# Generated by Django 5.0.7 on 2024-08-05 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_plasticcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plasticcard',
            name='card_number',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='plasticcard',
            name='card_type',
            field=models.CharField(choices=[('uzcard', 'Uzcard'), ('humo', 'Humo')], default='uzcard', max_length=15),
        ),
    ]