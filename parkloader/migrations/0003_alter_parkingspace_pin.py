# Generated by Django 4.1.7 on 2024-12-12 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkloader', '0002_vehiclebooking_alter_parkinglot_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingspace',
            name='pin',
            field=models.CharField(default=' pin your location', max_length=400),
        ),
    ]