from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Q,Count
from django.http import HttpResponseRedirect
import bcrypt
from directorate.models import Alumni,College,Passingyear,Events
from datetime import *
from django.core.mail import EmailMultiAlternatives
from Alumni_Tracking_System.settings import EMAIL_HOST_USER


        

# Create your views here.
def AlumniLogin(request):
    try:
        print("manav")
        result = request.session['Alumni']
        print("man")
        return redirect("alumni-dashboard")
    except Exception as e:
        return render(request,'LoginTemplates/AlumniLogin.html')

def Logout(request):
    request.session.flush()
    return render(request,'LoginTemplates/AlumniLogin.html')




def CheckAlumniLogin(request):
    

    try:
        emailid = request.POST['emailid']
        
        password = request.POST['password']
        admin=Alumni.objects.get(email=emailid,verification_status=1)
        # # Adminlogins.ob
        if bcrypt.checkpw(password.encode("utf8"), admin.password.encode("utf8")):
            request.session['Alumni']=admin.id
            return redirect('alumni-dashboard')

        else:
            return render(request, "LoginTemplates/AlumniLogin.html", { 'msg': 'Invalid Userid or Password'})

    except Exception as e:
          print(e)
          Logout(request) 
          return render(request, "LoginTemplates/AlumniLogin.html", {'msg': 'Server Error'})

def Alumnidashboard(request):
    
    try:
        result = request.session['Alumni']
        alumni=Alumni.objects.get(id=result)
        college = College.objects.all()
        year = Passingyear.objects.all()
        events=Events.objects.filter(cdid=alumni.collegeid.id) 

        return render(request, "DashboardTemplates/AlumniDashboard.html",{'events':events,'alumni':alumni,'college':college,'year':year})
    except  Exception as e:
        Logout(request) 
        return redirect('alumni-login')


def AlumniRegister(request):
    college = College.objects.all()
    year = Passingyear.objects.all()
    
    return render(request, "LoginTemplates/Alumniregistration.html",{'college':college,'year':year})

def Registeration(request):
   try: 
    clg = int(request.POST['collegeid'])
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    passoutyear = request.POST['passoutyear']
    exp = request.POST['exp']
    currentjob = request.POST['currentjob']
    salt= bcrypt.gensalt()
    hashed = bcrypt.hashpw(phone.encode("utf8"),salt)
    hashed=(hashed.decode("utf8"))
    collegeid = College.objects.get(id=clg).id
    t=Alumni.objects.create(collegeid_id = College.objects.get(id=clg).id , name=name,email=email,phone=phone,passout_year=passoutyear,experience=exp,current_job=currentjob,verification_status=0,registration_status=1,password=hashed) 
    t.save()
    subject="Login Credentials"
    content="You are now successfully registered Your default login id is {} and Password is {}".format(email,phone)
    msg = EmailMultiAlternatives(f'{subject}',f'{content}',EMAIL_HOST_USER,[f'{email}'])
    msg.send()
    
    return JsonResponse({"status": "done"}, status=200)
   except Exception as e:
       return JsonResponse({"error": "Status not upadated "}, status=400)



def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def AlumniUpdatepassword(request):
    try:
        result = request.session['Alumni']
        password=(Alumni.objects.get(id=result)).password
        if is_ajax(request=request) and request.method == "POST":
            currentpwd= request.POST.get('currentpwd',None)
            newpwd = request.POST.get('newpwd',None)
            confirmpwd = request.POST.get('confirmpwd',None)
            if bcrypt.checkpw(currentpwd.encode("utf8"), password.encode("utf8") ):
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(newpwd.encode("utf8"),salt)
                hashed=(hashed.decode("utf8"))
                Alumni.objects.filter(id=result).update(password=hashed) 
            else:
                return JsonResponse({"error": "Status not upadated"}, status=400)

             
            Logout(request)
            return JsonResponse({"status": "done"}, status=200)

    # some error occured
        return JsonResponse({"error": "Status not upadated"}, status=400)
    except  Exception as e:
            return JsonResponse({"error": "Status not upadated "}, status=400)


def AlumniUpdateprofile(request):
    
    try:
        result = request.session['Alumni']
        
        if is_ajax(request=request) and request.method == "POST":
            clg = int(request.POST['collegeid'])
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            passoutyear = request.POST['passoutyear']
            exp = request.POST['exp']
            currentjob = request.POST['currentjob']
        
            Alumni.objects.filter(id=result).update(collegeid_id = College.objects.get(id=clg).id , name=name,email=email,phone=phone,passout_year=passoutyear,experience=exp,current_job=currentjob) 
                 
            # EmailService.SendMail(email_id,"Hi your default password is {}".format(contact_number))


            

            return JsonResponse({"status": "done"}, status=200)

    # some error occured
        return JsonResponse({"error": "User Exists"}, status=400)
    except  Exception as e:
            return JsonResponse({"error": "User Exists"}, status=400)



def Groupchat(request):
    
    try:
        result = request.session['Alumni']
        alumni=Alumni.objects.get(id=result)
        

            

        return render(request, "Groupchat.html",{'alumni':alumni})

    except Exception as e:
          print("error",e)
          Logout(request) 
          return render(request, "LoginTemplates/AlumniLogin.html", {'msg': 'Server Error'})

