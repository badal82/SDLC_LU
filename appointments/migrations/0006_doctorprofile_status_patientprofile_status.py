# Generated by Django 4.2.6 on 2024-02-27 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0005_remove_appointment_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='status',
            field=models.CharField(choices=[('requested', 'Requested'), ('approved', 'Approved'), ('visited', 'Visited')], default='requested', max_length=20),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='status',
            field=models.CharField(choices=[('requested', 'Requested'), ('approved', 'Approved'), ('visited', 'Visited')], default='requested', max_length=20),
        ),
    ]
