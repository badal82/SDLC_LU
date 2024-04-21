from django.contrib import messages
from django.contrib import admin
from .models import DoctorProfile, PatientProfile, Appointment
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.generic.detail import DetailView
from django.urls import path
from django.template.response import TemplateResponse

# Register your models here.

admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)


# Define the admin class
class AppointmentAdmin(admin.ModelAdmin):
    list_filter = ("patient", "doctor", "date_time", "status")
    change_list_template = "view.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("statistics/", self.statistics_view),
            # path("", self.view),
        ]
        return my_urls + urls

    def view(self, request):
        appointments_list = []
        allapointments=Appointment.objects.all().filter(doctor_id=request.user.id)
        for item in allapointments: 
            thisdict={
            "patient_name": item.patient.username,
            "status": item.status,
            "date_time": item.date_time
            }
            appointments_list.append(thisdict)
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            #    key=value,
            doctor_name = DoctorProfile.objects.filter(user_id=request.user.id).first().name,
            appointments = appointments_list,
            custom_links =[
                {'name': 'Statistics', 'url': 'statistics'},
            ]
        )
        return TemplateResponse(request, "view.html", context)

    def statistics_view(self, request):
        appointments_list = []
        allapointments=Appointment.objects.all().filter(doctor_id=request.user.id)
        for item in allapointments: 
            thisdict={
            "patient_name": item.patient.username,
            "status": item.status,
            "date_time": item.date_time
            }
            appointments_list.append(thisdict)
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            #    key=value,
            doctor_name = DoctorProfile.objects.filter(user_id=request.user.id).first().name,
            appointments = appointments_list
        )
        return TemplateResponse(request, "statistics.html", context)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # create form
            self.exclude = (
                "status",
                "patient",
            )
        else:  # update form
            self.exclude = ()

        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if change:  # Update form
            if obj.patient_id == request.user.id:
                raise Exception("Patient cannot update the Appointment details")
        else:  # Create form
            obj.patient_id = request.user.id

        obj.save()
        if change:  # Send email only if it's an update (i.e., approval)
            subject = 'Your appointment has been approved'
            message = render_to_string('approval_email.html', {'patient_name': PatientProfile.objects.filter(user_id=obj.patient_id)[0].name})
            patient_email = obj.patient.email  # Assuming you have a field for patient's email in the Appointment model
            send_mail(subject, message, "angeldana2017@gmail.com", [patient_email],fail_silently=False)


admin.site.register(Appointment, AppointmentAdmin)

# modify admin site UI name 
admin.site.site_title = 'SDLC'
admin.site.site_header = 'Healthcare Appointment System'
admin.site.index_title = 'Profile' 

