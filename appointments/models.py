# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    availability = models.CharField(
        max_length=100
    )  # You might want to use a more suitable field for availability
    icon_url = models.CharField(max_length=1000)
    bio = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon_url = models.CharField(max_length=1000)


class Status(models.TextChoices):
    REQUESTED = "requested", "Requested"
    APPROVED = "approved", "Approved"
    VISITED = "visited", "Visited"
    REJECTED = "Rejected", "Rejected"

class Appointment(models.Model):
    def __str__(self):
        # Customize the string representation here
        return f"Appointment for {self.patient.username} with {self.doctor.username}"

    patient = models.ForeignKey(
        User, related_name="appointments", on_delete=models.CASCADE
    )
    doctor = models.ForeignKey(
        User, related_name="doctor_appointments", on_delete=models.CASCADE
    )
    date_time = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.REQUESTED
    )


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ["status"]  # Exclude status field from the form by default
        widgets = {"status": forms.HiddenInput()}  # Set status field as hidden

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Exclude status field from form if instance is provided (edit mode)
            # del self.fields['status']
            self.fields["status"].widget = forms.Select(choices=Status.choices)
        else:
            # Set status field as hidden for create form with default value
            self.fields["status"].widget = forms.HiddenInput()
            self.fields["status"].initial = Status.REQUESTED
