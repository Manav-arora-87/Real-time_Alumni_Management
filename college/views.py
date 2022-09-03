from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Q,Count
from django.http import HttpResponseRedirect
import bcrypt
from directorate.models import Alumni,College,Directorate,Email,Passingyear,Events
from django.core.mail import EmailMultiAlternatives
from Alumni_Tracking_System.settings import EMAIL_HOST_USER

from datetime import *

# Create your views here.
def CollegeLogin(request):
    try:
        result = request.session['College']
        return redirect("college-dashboard")
    except Exception as e:
        print(e)
        return render(request,'LoginTemplates/CollegeLogin.html')

def Logout(request):
    request.session.flush()
    return render(request,'LoginTemplates/CollegeLogin.html')

def CheckCollegeLogin(request):
    

    try:
        emailid = request.POST['emailid']
        
        password = request.POST['password']
        admin=College.objects.get(email=emailid)
        # # Adminlogins.ob
        if bcrypt.checkpw(password.encode("utf8"), admin.password.encode("utf8")):
             request.session['College']=admin.id
             return redirect('college-dashboard')
        else:
            return render(request, "DashboardTemplates/CollegeDashboard.html", { 'msg': 'Invalid Userid or Password'})
        

    except Exception as e:
          Logout(request) 
          print(e)
          return render(request, "LoginTemplates/CollegeLogin.html", {'msg': 'Server Error'})

def Collegedashboard(request):
    
    try:
        result = request.session['College']
        py=reversed(Passingyear.objects.all()) 
        clgname = College.objects.get(id=result).name
        b=int(request.POST.get('year',0))
        status=int(request.POST.get('status',3))
        if(b ==0 and status==3):
            alumni = Alumni.objects.filter(Q(collegeid=result))
            return render(request, "DashboardTemplates/CollegeDashboard.html",{'status':status,'clgname':clgname,'years':py,'b':b,'alumni':alumni})
        elif(b==0 and status!=3):
             alumni = Alumni.objects.filter(Q(collegeid=result)).filter(Q(verification_status=status))
             return render(request, "DashboardTemplates/CollegeDashboard.html",{'status':status,'clgname':clgname,'years':py,'b':b,'alumni':alumni})
        elif(b!=0 and status==3):
             alumni = Alumni.objects.filter(Q(collegeid=result)).filter(Q(passout_year=b))
             return render(request, "DashboardTemplates/CollegeDashboard.html",{'status':status,'clgname':clgname,'years':py,'b':b,'alumni':alumni})
        else:
            alumni = Alumni.objects.filter(Q(collegeid=result)).filter(Q(passout_year=b)).filter(Q(verification_status=status))
            return render(request, "DashboardTemplates/CollegeDashboard.html",{'status':status,'clgname':clgname,'years':py,'b':b,'alumni':alumni})

    
    except  Exception as e:
        Logout(request) 
        return redirect('college-login')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def update_verfication(request):
    try:
        result = request.session['College']
        if is_ajax(request=request) and request.method == "POST":
            status=None
            if request.POST['data']=="0":
                status=1
                content="You are now Verified"
            else:
                status=0
                content="You are now Unverified"
            subject="Verification Update"
            mail=Alumni.objects.get(id=request.POST['regid']).email
            Alumni.objects.filter(id=request.POST['regid']).update(verification_status=status)
            msg = EmailMultiAlternatives(f'{subject}',f'{content}',EMAIL_HOST_USER,[f'{mail}'])
            msg.send()
            return JsonResponse({"status": "done"}, status=200)

        return JsonResponse({"error": "Status not upadated"}, status=400)
    except  Exception as e:
            return JsonResponse({"error": "Status not upadated "}, status=400)


def MailInbox(request):
    try:
            result = request.session['College']
            clgname = College.objects.get(id=result).name

            alumni=Alumni.objects.filter(Q(collegeid=result))
            allmails=reversed(Email.objects.filter(Q(cdid=result)))
            return render(request, "College/Mail.html",{'clgname':clgname,'alumni':alumni,'allmails':allmails})
    except  Exception as e:
        Logout(request) 
        return redirect('college-login')



def SendMail(request):
    
    try:
        result = request.session['College']
        if request.method == "POST":
            
            email= request.POST.getlist('email')
            subject = request.POST.get('subject')
            content = request.POST.get('content')
            # html = request.POST.get('html')
            for mail in email:

                msg = EmailMultiAlternatives(f'{subject}',f'{content}',EMAIL_HOST_USER,[f'{mail}'])
                
                msg.send()
                Email.objects.create(email=mail,date=date.today(),subject=subject,content=content,cdid=result)   
            
        return redirect('college-dashboard')
    except  Exception as e:
        Logout(request) 
        return redirect('college-login')



def Update_Password(request):
    try:
        result = request.session['College']
        password=(College.objects.get(id=result)).password
        if is_ajax(request=request) and request.method == "POST":
            currentpwd= request.POST.get('currentpwd',None)
            newpwd = request.POST.get('newpwd',None)
            confirmpwd = request.POST.get('confirmpwd',None)
            if bcrypt.checkpw(currentpwd.encode("utf8"), password.encode("utf8") ):
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(newpwd.encode("utf8"),salt)
                hashed=(hashed.decode("utf8"))
                College.objects.filter(id=result).update(password=hashed) 
            else:
                return JsonResponse({"error": "Status not upadated"}, status=400)

             
            Logout(request)
            return JsonResponse({"status": "done"}, status=200)

    # some error occured
        return JsonResponse({"error": "Status not upadated"}, status=400)
    except  Exception as e:
            return JsonResponse({"error": "Status not upadated "}, status=400)



def ClgEventSubmit(request):
    try:
        result = request.session['College']
        efile=request.FILES['eventfile']
        event=str(efile)
        t=Events.objects.create(eventfile=event,cdid=result)   

        F = open('D:/REAL-TIME_ALUMNI_MANAGEMENT/assets/events/'+event,"wb")
      
        
       
        for chunk in efile.chunks():
            F.write(chunk)
        F.close()
            
    
        return redirect('college-dashboard')

    except Exception as e:
        return render(request,"DashboardTemplates/CollegeDashboard.html")

