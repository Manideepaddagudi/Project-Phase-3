from django import forms
from django.contrib.auth.models import User
from . import models


# for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


# for Doctor related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = models.Doctor
        fields = ['address', 'mobile', 'department', 'status', 'profile_pic']


# for Patient related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class PatientForm(forms.ModelForm):
    # this is the extrafield for linking patient and their assigend doctor
    # this will show dropdown __str__ method doctor model is shown on html so override it
    # to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    assignedDoctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all(
    ).filter(status=True), empty_label="Name and Department", to_field_name="user_id")

    class Meta:
        model = models.Patient
        fields = ['address', 'mobile', 'status', 'symptoms', 'profile_pic']


# for Technician related form
class TechnicianUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }


class TechnicianForm(forms.ModelForm):
    # this is the extrafield for linking Technicina with the doctor
    assignedDoctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all(
    ).filter(status=True), empty_label="Name and Department", to_field_name="user_id")

    class Meta:
        model = models.Technician
        fields = ['address', 'mobile', 'status', 'profile_pic']


class AppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(
        status=True), empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId = forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(
        status=True), empty_label="Patient Name and Symptoms", to_field_name="user_id")

    class Meta:
        model = models.Appointment
        fields = ['description', 'status']


class PatientAppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(
        status=True), empty_label="Doctor Name and Department", to_field_name="user_id")

    class Meta:
        model = models.Appointment
        fields = ['description', 'status']


# for lab tests form
class TestForm(forms.ModelForm):
    technicianId = forms.ModelChoiceField(queryset=models.Technician.objects.all(
    ).filter(status=True), empty_label="Tecnician Name", to_field_name="user_id")
    patientId = forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(
        status=True), empty_label="Patient Name and Symptoms", to_field_name="user_id")

    class Meta:
        model = models.Test
        fields = ['description', 'status', 'result']

# for contact us page


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(
        max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
