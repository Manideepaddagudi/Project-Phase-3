from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from . import forms, models
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
# Create your views here.

# View for home page


def home_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('afterlogin')
    return render(request, 'hospital/index.html')

# for checking user is doctor , patient or admin(by submit button)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()


def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


def is_technician(user):
    return user.groups.filter(name='TECHNICIAN').exists()


# for showing signup/login button for admin(by submit)
def adminclick_view(request):
    if request.user.is_authenticated and is_admin(request.user):
        return redirect('admin-dashboard')
    context = {'error': 'Account Not Found, Please Register'}
    return render(request, 'hospital/adminclick.html', context=context)


# for showing signup/login button for doctor(by submit)
def doctorclick_view(request):
    if is_doctor(request.user):
        if accountapproval := models.Doctor.objects.all().filter(user_id=request.user.id, status=True):
            return redirect('doctor-dashboard')
        else:
            return render(request, 'hospital/doctor_wait_for_approval.html')
    context = {'error': 'Account Not Found, Please Register'}
    return render(request, 'hospital/doctorclick.html', context=context)


# for showing signup/login button for patient(by submit)
def patientclick_view(request):
    if is_patient(request.user):
        if accountapproval := models.Patient.objects.all().filter(user_id=request.user.id, status=True):
            return redirect('patient-dashboard')
        else:
            return render(request, 'hospital/patient_wait_for_approval.html')
    return render(request, 'hospital/patientclick.html')

# for showing signup/login button for technician(by submit)


def technicianclick_view(request):
    if is_technician(request.user):
        if accountapproval := models.Technician.objects.all().filter(user_id=request.user.id, status=True):
            return redirect('technician-dashboard')
        else:
            return render(request, 'hospital/technician_wait_for_approval.html')
    return render(request, 'hospital/technicianclick.html')

# Now work for signup views


def admin_signup_view(request):  # sourcery skip: extract-method
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request, 'hospital/adminsignup.html', {'form': form})


def doctor_signup_view(request):  # sourcery skip: extract-method
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor = doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request, 'hospital/doctorsignup.html', context=mydict)


def patient_signup_view(request):  # sourcery skip: extract-method
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient = patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request, 'hospital/patientsignup.html', context=mydict)


def technician_signup_view(request):  # sourcery skip: extract-method
    userForm = forms.TechnicianUserForm()
    technicianForm = forms.TechnicianForm()
    mydict = {'userForm': userForm, 'technicianForm': technicianForm}
    if request.method == 'POST':
        userForm = forms.TechnicianUserForm(request.POST)
        technicianForm = forms.TechnicianForm(request.POST, request.FILES)
        if userForm.is_valid() and technicianForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            technician = technicianForm.save(commit=False)
            technician.user = user
            technician.assignedDoctorId = request.POST.get('assignedDoctorId')
            technician = technician.save()
            my_technician_group = Group.objects.get_or_create(
                name='TECHNICIAN')
            my_technician_group[0].user_set.add(user)
        return HttpResponseRedirect('technicianlogin')
    return render(request, 'hospital/techniciansignup.html', context=mydict)


# ---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):  # sourcery skip: use-named-expression
    if is_admin(request.user):
        return redirect('admin-dashboard')

    elif is_doctor(request.user):
        accountapproval = models.Doctor.objects.all().filter(
            user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request, 'hospital/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountapproval = models.Patient.objects.all().filter(
            user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request, 'hospital/patient_wait_for_approval.html')

    elif is_technician(request.user):
        accountapproval = models.Technician.objects.all().filter(
            user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('technician-dashboard')
        else:
            return render(request, 'hospital/technician_wait_for_approval.html')


# ---------------------------------------------------------------------------------
# ------------------------ ADMIN RELATED VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    # for both table in admin dashboard
    doctors = models.Doctor.objects.all().order_by('-id')

    patients = models.Patient.objects.all().order_by('-id')
    technicians = models.Technician.objects.all().order_by('-id')
    # for three cards
    doctorcount = models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount = models.Doctor.objects.all().filter(status=False).count()

    patientcount = models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount = models.Patient.objects.all().filter(status=False).count()

    techniciancount = models.Technician.objects.all().filter(status=True).count()
    pendingtechniciancount = models.Technician.objects.all().filter(status=False).count()

    appointmentcount = models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount = models.Appointment.objects.all().filter(status=False).count()
    mydict = {
        'doctors': doctors,
        'patients': patients,
        'technicians': technicians,
        'doctorcount': doctorcount,
        'pendingdoctorcount': pendingdoctorcount,
        'patientcount': patientcount,
        'pendingpatientcount': pendingpatientcount,
        'techniciancount': techniciancount,
        'pendingtechniciancount': pendingtechniciancount,
        'appointmentcount': appointmentcount,
        'pendingappointmentcount': pendingappointmentcount,
        'techs_and_docs': zip(doctors,technicians),
    }
    return render(request, 'hospital/admin_dashboard.html', context=mydict)


# this view for doctor sidebar click on admin page


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request, 'hospital/admin_doctor.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors = models.Doctor.objects.all().filter(status=True)
    return render(request, 'hospital/admin_view_doctor.html', {'doctors': doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            doctor = doctorForm.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request, 'hospital/admin_add_doctor.html', context=mydict)



# ---------------------------------------------------------------------------------
# ------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
# ---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request, 'hospital/aboutus.html')


def contactus_view(request):
    sub = forms.ContactusForm()
    return render(request, 'hospital/contactus.html', {'form': sub})
