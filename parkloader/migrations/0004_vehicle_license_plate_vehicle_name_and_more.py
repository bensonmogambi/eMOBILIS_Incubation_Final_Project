# Generated by Django 4.1.7 on 2024-12-12 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parkloader', '0003_parkinglot_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='license_plate',
            field=models.CharField(default='UNKNOWN', max_length=20),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='name',
            field=models.CharField(default='Your name', max_length=100),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='parking_lot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='parkloader.parkinglot'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(choices=[('lorry', 'Lorry'), ('van', 'Van'), ('matatu', 'Matatu'), ('personal', 'Personal')], default='car', max_length=20),
        ),
    ]
