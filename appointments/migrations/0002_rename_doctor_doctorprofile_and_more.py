# Generated by Django 4.2.6 on 2024-02-27 17:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Doctor',
            new_name='DoctorProfile',
        ),
        migrations.RenameModel(
            old_name='Patient',
            new_name='PatientProfile',
        ),
    ]
