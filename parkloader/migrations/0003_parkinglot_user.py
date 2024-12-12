# Generated by Django 4.1.7 on 2024-12-11 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parkloader', '0002_remove_parkinglot_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkinglot',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]