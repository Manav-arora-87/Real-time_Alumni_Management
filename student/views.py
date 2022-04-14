from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Q,Count
from django.http import HttpResponseRedirect
import bcrypt
from directorate.models import Alumni,College,Directorate,Email,Passingyear,Events,Student,Articles,Posts,Nstiposts
from django.core.mail import EmailMultiAlternatives
from Alumni_Tracking_System.settings import EMAIL_HOST_USER

from datetime import *

# Create your views here.
def StudentLogin(request):
    try:
        result = request.session['student']
        return redirect("student-dashboard")
    except Exception as e:
        print(e)
        return render(request,'LoginTemplates/StudentLogin.html')

def Logout(request):
    request.session.flush()
    return render(request,'LoginTemplates/StudentLogin.html')

def CheckStudentLogin(request):
    

    try:
        emailid = request.POST['emailid']
        
        password = request.POST['password']
        print(emailid,password) 
        admin=Student.objects.get(emailid=emailid)
        # # Adminlogins.ob
        if bcrypt.checkpw(password.encode("utf8"), admin.password.encode("utf8")):
             request.session['student']=admin.id
             return redirect('student-dashboard')
        else:
            return render(request, "DashboardTemplates/StudentDashboard.html", { 'msg': 'Invalid Userid or Password'})
        

    except Exception as e:
          print("error",e)
          Logout(request) 
          return render(request, "LoginTemplates/StudentLogin.html", {'msg': 'Server Error'})

def Studentdashboard(request):
    
    try:
        result = request.session['student']
        posts=reversed(Posts.objects.all())
        articles=reversed(Articles.objects.all())

        return render(request, "DashboardTemplates/StudentDashboard.html",{'posts':posts,'articles':articles})

    
    except  Exception as e:
        print("erroe",e)
        Logout(request) 
        return redirect('student-login')


def StudentAlumniprofile(request):
    
    try:
        result = request.session['student']
        alumni=Alumni.objects.all()
        print(alumni)
        return render(request, "studentalumniprofile.html",{'alumni':alumni})

    
    except  Exception as e:
        print("erroe",e)
        Logout(request) 
        return redirect('student-login')


