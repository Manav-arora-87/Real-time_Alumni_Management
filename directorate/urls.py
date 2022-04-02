from os import name
from django.contrib import admin
from django.urls import path
from directorate import views


urlpatterns = [

    path('directorate-login/',views.DirectorateLogin,name='directorate-login'),
    path('directorate-checklogin',views.CheckDirectorateLogin),
    path('directorate-dashboard/',views.Directoratedashboard,name='directorate-dashboard'),
    path('logout/',views.Logout,name='logout'),
   
    path('mailinbox/',views.MailInbox,name='mail-inbox'),
    path('sendmail/',views.SendMail,name='send-mail'),
  
    path('alumnidetails/',views.AlumniDetails,name='alumni-details'),
    path('submitevents/',views.EventSubmit, name="submit-event"),
  
    path('directorate-changepassword',views.Update_Password,name='directorate-changepassword'),
   
    # path('filter/',views.Filter, name="filter"),
]
