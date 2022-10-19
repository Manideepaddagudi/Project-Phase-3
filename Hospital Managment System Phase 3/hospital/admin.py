from django.contrib import admin
from .models import Doctor,Patient,Appointment,PatientDischargeDetails, Technician, Test
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)


class TechnicianAdmin(admin.ModelAdmin):
    pass
admin.site.register(Technician, TechnicianAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class TestAdmin(admin.ModelAdmin):
    pass
admin.site.register(Test, TestAdmin)
class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)
from django.contrib import admin

# Register your models here.
