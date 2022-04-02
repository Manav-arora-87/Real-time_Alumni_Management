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
def DTEportal(request):
    events=Events.objects.filter(cdid=0)   
    # events=Events.objects.all()   
    return render(request,'DTEportal.html',{'events':events})
