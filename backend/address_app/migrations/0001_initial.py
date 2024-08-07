# Generated by Django 5.0.7 on 2024-07-17 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('county', models.CharField(max_length=255)),
                ('residential', models.CharField(max_length=255)),
                ('neighbourhood', models.CharField(max_length=255)),
                ('road', models.CharField(max_length=255)),
                ('house_number', models.CharField(max_length=255)),
                ('amenity', models.CharField(max_length=255)),
                ('shop', models.CharField(max_length=255)),
                ('man_made', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
                'db_table': 'locations',
            },
        ),
    ]
