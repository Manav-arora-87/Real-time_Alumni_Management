from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.db.models import Q,Count
from django.http import HttpResponseRedirect
import bcrypt
import uuid , os
from .models import Alumni,College,Directorate,Email,Events,Passingyear,Nstiposts,Articles
from datetime import *
from django.core.mail import EmailMultiAlternatives
from Alumni_Tracking_System.settings import EMAIL_HOST_USER

# Create your views here.
def DirectorateLogin(request):
    try:
        result = request.session['directorate']
        return redirect("directorate-dashboard")
    except Exception as e:
        return render(request,'LoginTemplates/DirectorateLogin.html')

def Logout(request):
    request.session.flush()
    return render(request,'LoginTemplates/DirectorateLogin.html')



def CheckDirectorateLogin(request):
    

    try:
        emailid = request.POST['emailid']
        
        password = request.POST['password']
        admin=Directorate.objects.get(email=emailid)
        # # Adminlogins.ob
        if bcrypt.checkpw(password.encode("utf8"), admin.password.encode("utf8")):
            request.session['Directorate']=admin.id
            return redirect('directorate-dashboard')
        # return render(request, "DashboardTemplates/DirectorateDashboard.html", {'msg': 'Server Error'})

        else:
             return render(request, "LoginTemplates/DirectorateLogin.html", { 'msg': 'Invalid Userid or Password'})

    except Exception as e:
          Logout(request) 
          return render(request, "LoginTemplates/DirectorateLogin.html", {'msg': 'Server Error'})





def Directoratedashboard(request):
    
    try:
        result = request.session['Directorate']
        college=College.objects.all()
        posts=reversed(Nstiposts.objects.all())
        articles=reversed(Articles.objects.filter(alumniid__isnull=True))

        
        return render(request, "DashboardTemplates/DirectorateDashboard.html",{'posts':posts,'articles':articles})
    except  Exception as e:
        Logout(request) 
        return redirect('directorate-login')



def Directoratecollegeview(request):
    
    try:
        result = request.session['Directorate']
        college=College.objects.all()
       
        
        return render(request, "College/dirctorate_college.html",{'college':college})
    except  Exception as e:
        print(e)
        Logout(request) 
        return redirect('directorate-login')




def NSTIjob(request):
    try:
        result = request.session['Directorate']
        picture = request.FILES['upload']
        print(picture)
        filename = str(uuid.uuid4())+picture.name[picture.name.rfind('.'):]
        t=Nstiposts.objects.create(post=filename,did_id=result)
        F = open('F:/REALTIME_ALUMNI_MANAGEMENT/assets/posts/'+filename,"wb")
        for chunk in picture.chunks():
             F.write(chunk)
             F.close()
              
            
        return JsonResponse({"status": "done"}, status=200)

    # some error occured
    except  Exception as e:
            print(e)
            return JsonResponse({"error": "Status not upadated "}, status=400)




def NSTIarticle(request):
    try:
        result = request.session['Directorate']
        heading = request.POST.get('heading',None)
        article = request.POST.get('article',None)
        t=Articles.objects.create(article=article,heading=heading)

        print(heading,article)
             
            
        return JsonResponse({"status": "done"}, status=200)

    # some error occured
    except  Exception as e:
            print(e)
            return JsonResponse({"error": "Status not upadated "}, status=400)





def MailInbox(request):
    try:
            result = request.session['Directorate']
            college=College.objects.all()
            allmails=Email.objects.all()
            return render(request, "Mail.html",{'college':college,'allmails':allmails})
    except  Exception as e:
        Logout(request) 
        return redirect('directorate-login')



def SendMail(request):
    
    try:
        result = request.session['Directorate']
        if request.method == "POST":
            
            email= request.POST.getlist('email')
            subject = request.POST.get('subject')
            content = request.POST.get('content')
            # html = request.POST.get('html')
            for mail in email:

                msg = EmailMultiAlternatives(f'{subject}',f'{content}',EMAIL_HOST_USER,[f'{mail}'])
                # msg.attach_alternative(html,"text/html")
                msg.send()
                Email.objects.create(email=mail,date=date.today(),subject=subject,content=content,cdid=0)   
            
        return redirect('mail-inbox')
    except  Exception as e:
        Logout(request) 
        return redirect('directorate-login')


def AlumniDetails(request):
    
    try:
        result = request.session['Directorate']
        clgs=College.objects.all()
        py=reversed(Passingyear.objects.all()) 

        a=int(request.POST.get('clgname',0))
        b=int(request.POST.get('year',0))
        if(a==0 and b==0):
            alumni=Alumni.objects.all()
            return render(request, "AlumniDetails.html",{'a':a,'b':b,'alumni':alumni,'years':py,'clgs':clgs})
        elif(a==0 and b!=0):
            alumni=Alumni.objects.filter(Q(passout_year=b))
            return render(request, "AlumniDetails.html",{'a':a,'b':b,'alumni':alumni,'years':py,'clgs':clgs})
        elif(b==0 and a!=0):
            alumni=Alumni.objects.filter(collegeid=a)
            return render(request, "AlumniDetails.html",{'a':a,'b':b,'alumni':alumni,'years':py,'clgs':clgs})
        else:
            alumni=Alumni.objects.filter(collegeid=a).filter(passout_year=b)
            return render(request, "AlumniDetails.html",{'a':a,'b':b,'alumni':alumni,'years':py,'clgs':clgs})

    except  Exception as e:
        Logout(request) 
        return redirect('directorate-login')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def EventSubmit(request):
    try:
        result = request.session['Directorate']
        efile=request.FILES['eventfile']
        event=str(efile)
        t=Events.objects.create(eventfile=event,cdid=0)   

        F = open('F:/DareToCode/Alumni_Tracking_System/assets/events/'+event,"wb")
      
        
       
        for chunk in efile.chunks():
            F.write(chunk)
        F.close()
            
    
        return redirect('directorate-dashboard')

    except Exception as e:
        return render(request,"DashboardTemplates/DirectorateDashboard.html")


def Update_Password(request):
    try:
        result = request.session['Directorate']
        password=(Directorate.objects.get(id=result)).password
        if is_ajax(request=request) and request.method == "POST":
            currentpwd= request.POST.get('currentpwd',None)
            newpwd = request.POST.get('newpwd',None)
            confirmpwd = request.POST.get('confirmpwd',None)
            if bcrypt.checkpw(currentpwd.encode("utf8"), password.encode("utf8") ):
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(newpwd.encode("utf8"),salt)
                hashed=(hashed.decode("utf8"))
                Directorate.objects.filter(id=result).update(password=hashed) 
            else:
                return JsonResponse({"error": "Status not upadated"}, status=400)

             
            Logout(request)
            return JsonResponse({"status": "done"}, status=200)

    # some error occured
        return JsonResponse({"error": "Status not upadated"}, status=400)
    except  Exception as e:
            return JsonResponse({"error": "Status not upadated "}, status=400)
