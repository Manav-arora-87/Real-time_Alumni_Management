from os import name
from django.contrib import admin
from django.urls import path
from Alumni import views


urlpatterns = [

    path('alumni-login/',views.AlumniLogin,name='alumni-login'),
    path('alumni-checklogin',views.CheckAlumniLogin),
    path('alumni-logout',views.Logout),
    path('alumni-dashboard/',views.Alumnidashboard,name='alumni-dashboard'),
    path('alumni-register/',views.AlumniRegister,name='alumni-register'),
    path('registeration/',views.Registeration,name='registeration'),
    path('alumni-changepassword/',views.AlumniUpdatepassword,name='alumni-changepassword'),
    path('alumni-updateprofile/',views.AlumniUpdateprofile,name='alumni-updateprofile'),
    path('alumni-grpchat/',views.Groupchat,name='alumni-grpchat'),
  
]
