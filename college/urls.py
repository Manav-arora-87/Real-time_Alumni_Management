from os import name
from django.contrib import admin
from django.urls import path
from college import views


urlpatterns = [

    path('college-login/',views.CollegeLogin,name='college-login'),
    path('college-checklogin',views.CheckCollegeLogin),
    path('collegelogout/',views.Logout),
    path('college-dashboard/',views.Collegedashboard,name='college-dashboard'),

    path('admin-update_surveyor_verfications',views.update_verfication,name='admin-update_surveyor_verfications'),

    path('clg_mailinbox/',views.MailInbox,name='clg_mail-inbox'),
    path('clg_sendmail/',views.SendMail,name='clg_send-mail'),
    path('clgsubmitevents/',views.ClgEventSubmit, name="submit-event"),
  
    path('college-changepassword',views.Update_Password,name='college-changepassword'),

]
