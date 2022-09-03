from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Q,Count
from django.http import HttpResponseRedirect
import bcrypt
import uuid,os
from directorate.models import Alumni,College,Passingyear,Events,Articles,Posts,Nstiposts
from datetime import *
from django.core.mail import EmailMultiAlternatives
from Alumni_Tracking_System.settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.tokens import PasswordResetTokenGenerator

import threading
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.views.generic import View
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
# from validate_email import validate_email
from django.contrib.auth.models import User

domain={'mitsgwl.ac.in','sgsits.ac.in'}

class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()       
       

# Create your views here.
def AlumniLogin(request):
    try:
        
        result = request.session['Alumni']
        
        return redirect("alumni-dashboard")
    except Exception as e:
        print("error",e)
        return render(request,'LoginTemplates/AlumniLogin.html')

def Logout(request):
    request.session.flush()
    return render(request,'LoginTemplates/AlumniLogin.html')




def CheckAlumniLogin(request):
    

    try:
        emailid = request.POST['emailid']
        
        password = request.POST['password']
        admin=Alumni.objects.get(email=emailid,is_active=1)
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
        articles=reversed(Articles.objects.filter(alumniid=result))
        posts=reversed(Posts.objects.filter(alumni_id=result))
        
        # college = College.objects.all()
        # year = Passingyear.objects.all()
        events=Events.objects.filter(cdid=alumni.collegeid.id) 

        return render(request, "DashboardTemplates/AlumniDashboard.html",{'posts':posts,'articles':articles,'events':events,'alumni':alumni})
    except  Exception as e:
        print("error",e)
        Logout(request) 
        return redirect('alumni-login')


def Alumniprofile(request):
    
    try:
        result = request.session['Alumni']
        alumni=Alumni.objects.get(id=result)
        # college = College.objects.all()
        # year = Passingyear.objects.all()
        events=Events.objects.filter(cdid=alumni.collegeid.id) 

        return render(request, "Alumniprofile.html",{'events':events,'alumni':alumni})
    except  Exception as e:
        print("error",e)
        Logout(request) 
        return redirect('alumni-login')



def AlumniRegister(request):
    
    return render(request, "LoginTemplates/Alumniregistration.html")



def Registeration(request):
   try: 
    clgemail = request.POST['clgmail']
    last= clgemail.split('@')
    if last[1] not in domain:
         return JsonResponse({"error": "Your coleege is not yet registered !!!"}, status=400)
        
    pwd = request.POST['password']
    salt= bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd.encode("utf8"),salt)
    hashed=(hashed.decode("utf8"))
    t=Alumni.objects.create(email=clgemail,is_active=0,collegeid_id = 1,password=hashed) #clgid needs to be removed
    t.save()
    current_site = get_current_site(request)
    email_subject = 'Active your Account'
    message = render_to_string('auth/activate.html',
                                   {
                                       'user': t,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(t.pk)),
                                       'token': generate_token.make_token(t)
                                   }
                                   )

    email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [clgemail]
        )

    EmailThread(email_message).start()
    messages.add_message(request, messages.SUCCESS,
                             'account created succesfully')

    return redirect('alumni-login') 
   except Exception as e:
     print (e)
     return JsonResponse({"error": "Status not upadated "}, status=400)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Alumni.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'account activated successfully')
            return redirect('alumni-login')
        return render(request, 'auth/activate_failed.html', status=401)



def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'





def Alumninstiposts(request):
    
    try:
        result = request.session['Alumni']
        posts=reversed(Nstiposts.objects.all())
        alumni=Alumni.objects.get(id=result)
       
        articles=reversed(Articles.objects.filter(alumniid__isnull=True))
        
        return render(request, "Alumni_nsti.html",{'alumni':alumni,'posts':posts,'articles':articles})
    except  Exception as e:
        print(e)
        Logout(request) 
        return redirect('directorate-login')



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




def Alumnipostarticle(request):
    try:
        result = request.session['Alumni']
        heading = request.POST.get('heading',None)
        article = request.POST.get('article',None)
        t=Articles.objects.create(article=article,alumniid_id=result,heading=heading)

        print(heading,article)
             
            
        return JsonResponse({"status": "done"}, status=200)

    # some error occured
    except  Exception as e:
            print(e)
            return JsonResponse({"error": "Status not upadated "}, status=400)




def Alumnipost(request):
    try:
        result = request.session['Alumni']
        picture = request.FILES['upload']
        filename = str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        t=Posts.objects.create(post=filename,alumni_id=result)
        F = open('D:/REAL-TIME_ALUMNI_MANAGEMENT/assets/posts/'+filename,"wb")
        for chunk in picture.chunks():
            F.write(chunk)
            F.close()
              
            
        return JsonResponse({"status": "done"}, status=200)

    # some error occured
    except  Exception as e:
            print(e)
            return JsonResponse({"error": "Status not upadated "}, status=400)






def AlumniUpdateprofile(request):
    
    try:
        result = request.session['Alumni']
        
        if is_ajax(request=request) and request.method == "POST":
        
            name = request.POST.get('name',None)
            phone = request.POST.get('phone',None)
            current_job = request.POST.get('current_job',None)
            currentjob_location = request.POST.get('currentjob_location',None)
            experience = request.POST.get('experience',None)
            github = request.POST.get('github',None)
            linkedin = request.POST.get('linkedin',None)
            twitter = request.POST.get('twitter',None)
            instagram = request.POST.get('instagram',None)
            print(name,phone,current_job,currentjob_location,experience,github,linkedin,twitter,instagram)
            Alumni.objects.filter(id=result).update(name=name,phone=phone,experience=experience,current_job=current_job,currentjob_location=currentjob_location,github=github,twiter=twitter,linkedin=linkedin,instagram=instagram) 
                 
            # EmailService.SendMail(email_id,"Hi your default password is {}".format(contact_number))


            

            return JsonResponse({"status": "done"}, status=200)

    # some error occured
        return JsonResponse({"error": "User Exists"}, status=400)
    except  Exception as e:
            print(e)
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

