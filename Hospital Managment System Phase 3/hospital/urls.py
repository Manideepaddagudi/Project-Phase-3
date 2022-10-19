from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.home_view, name='home'),

    # add about us and contact us page paths
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),

    # add doctor, patient, admin click pages url path

    path('adminclick', views.adminclick_view, name='adminclick'),
    path('doctorclick', views.doctorclick_view, name='doctorclick'),
    path('patientclick', views.patientclick_view, name='patientclick'),
    path('technicianclick', views.technicianclick_view, name='technicianclick'),

    # add admin, patient, doctor registration url
    path('adminsignup', views.admin_signup_view, name='adminsignup'),
    path('doctorsignup', views.doctor_signup_view, name='doctorsignup'),
    path('patientsignup', views.patient_signup_view, name='patientsignup'),
    path('techniciansignup', views.technician_signup_view, name='techniciansignup'),

    # admin doctor and patient login
    path('adminlogin', LoginView.as_view(
        template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(
        template_name='hospital/doctorlogin.html')),
    path('patientlogin', LoginView.as_view(
        template_name='hospital/patientlogin.html')),
    path('technicianlogin', LoginView.as_view(
        template_name='hospital/technicianlogin.html')),

    # after login and logout
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('logout', LogoutView.as_view(
        template_name='hospital/index.html'), name='logout'),

    # admin dashboard
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),


    # # Doctor related admin work
    path('admin-doctor', views.admin_doctor_view, name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view,
         name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>',
         views.delete_doctor_from_hospital_view, name='delete-doctor-from-hospital'),
    path('admin-add-doctor', views.admin_add_doctor_view, name='admin-add-doctor'),



]



