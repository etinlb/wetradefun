# Create your views here.

import datetime, random, sha


from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
from django.contrib import messages

from user.forms import *


handler500 = 'djangotoolbox.errorviews.server_error'

def index(request):
    return HttpResponse('THIS MESSAGE WILL HAVE TO DO UNTIL I FIGURE OUT HOW TO WORK TEMPLATES PROPERLY')


def log_in(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
    		user = authenticate(username=usern, password=passw)
    		if user is not None:
        		if user.is_active:
            		login(request, user)
            		return HttpResponse("I GO TO SUCCESSPAGE")
            		
            	else:
            		return HttpResponse("LOL UR ACC DISABLED")

   			else:
        		return render_to_response('users/sign.html', {
        		'form': form,
    			},
    			context_instance=RequestContext(request))	
        else: 
            if "__all__" in form._errors:
                messages.add_message(request, messages.ERROR, form._errors['__all__'])

    else:
    	form = LoginForm()

def save(request, users_name):
    u=UserProfile(name=users_name)
    u.save()
    return HttpResponse("You save a user. Please load his name by using id %s." % u.id)

def load(request, users_id):
    u=Users.objects.get(id=users_id)
    return HttpResponse("You load a user whose name is %s." % u.name)

