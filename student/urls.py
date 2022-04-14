from os import name
from django.contrib import admin
from django.urls import path
from student import views


urlpatterns = [

    path('student-login/',views.StudentLogin,name='student-login'),
    path('student-checklogin',views.CheckStudentLogin),
    path('studentlogout/',views.Logout),
    path('student-dashboard/',views.Studentdashboard,name='student-dashboard'),
    path('student-alumniprofiles/',views.StudentAlumniprofile,name='student-alumniprofiles'),

]
